import boto3
import os
import json
from PIL import Image, ImageDraw

class TextractPOC:
    def __init__(self):
        """
        Initialize Textract and S3 clients with specified region
        Assumes AWS credentials are configured via AWS CLI or environment variables
        """
        self.textract_client = boto3.client('textract')

    def detect_document_text(self, image_path):
        """
        Detect and extract text from document images
        
        :param image_path: Path to the local image file
        :return: Extracted text blocks
        """
        with open(image_path, 'rb') as document:
            image_bytes = document.read()
        
        response = self.textract_client.detect_document_text(Document={'Bytes': image_bytes})
        
        print("\n--- Document Text Detection Results ---")
        for item in response['Blocks']:
            if item['BlockType'] == 'LINE':
                print(item['Text'])
        
        return response['Blocks']

    def analyze_document(self, image_path):
        """
        Analyze document with form and table detection
        
        :param image_path: Path to the local image file
        :return: Detected forms and tables
        """
        with open(image_path, 'rb') as document:
            image_bytes = document.read()
        
        response = self.textract_client.analyze_document(
            Document={'Bytes': image_bytes},
            FeatureTypes=['FORMS', 'TABLES']
        )
        
        print("\n--- Document Analysis Results ---")
        
        # Process Forms
        print("\nForm Key-Value Pairs:")
        for item in response['Blocks']:
            if item['BlockType'] == 'KEY_VALUE_SET' and item['EntityTypes'][0] == 'KEY':
                key = item['Text'] if 'Text' in item else 'Unknown Key'
                value_block = next((b for b in response['Blocks'] 
                                    if b['BlockType'] == 'KEY_VALUE_SET' 
                                    and b['EntityTypes'][0] == 'VALUE' 
                                    and b['Relationships'][0]['Ids'][0] == item['Id']), None)
                
                if value_block and 'Text' in value_block:
                    print(f"{key}: {value_block['Text']}")
        
        # Process Tables
        print("\nTable Cells:")
        table_blocks = [block for block in response['Blocks'] if block['BlockType'] == 'TABLE']
        for table_index, table in enumerate(table_blocks, 1):
            print(f"\nTable {table_index}:")
            cell_blocks = [block for block in response['Blocks'] 
                           if block['BlockType'] == 'CELL' and block['Relationships'][0]['Ids'][0] == table['Id']]
            
            for cell in cell_blocks:
                print(f"Cell: {cell.get('Text', 'Empty')}")
        
        return response

    def analyze_id(self, image_path):
        """
        Analyze identity documents like passports or driver's licenses
        
        :param image_path: Path to the local ID document image
        :return: Extracted ID information
        """
        with open(image_path, 'rb') as document:
            image_bytes = document.read()
        
        response = self.textract_client.analyze_id(DocumentPages=[{'Bytes': image_bytes}])
        
        print("\n--- ID Document Analysis Results ---")
        for result in response['IdentityDocuments']:
            for field in result['IdentityDocumentFields']:
                print(f"{field['Type']['Text']}: {field.get('ValueDetection', {}).get('Text', 'N/A')}")
        
        return response

    def visualize_document_geometry(self, image_path, blocks):
        """
        Visualize detected text blocks on the original image
        
        :param image_path: Path to the original image
        :param blocks: Textract detected blocks
        """
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        width, height = image.size

        for block in blocks:
            if block['BlockType'] in ['WORD', 'LINE']:
                bbox = block['Geometry']['BoundingBox']
                
                # Convert normalized coordinates to pixel coordinates
                left = bbox['Left'] * width
                top = bbox['Top'] * height
                right = left + (bbox['Width'] * width)
                bottom = top + (bbox['Height'] * height)
                
                # Draw bounding box
                draw.rectangle([left, top, right, bottom], outline='red', width=2)
                
                # Optional: Add text to the image
                if 'Text' in block:
                    draw.text((left, top-10), block['Text'], fill='blue')

        output_path = 'textract_geometry_visualization.jpg'
        image.save(output_path)
        print(f"\nGeometry visualization saved to {output_path}")

def main():
    
    # Initialize Textract POC
    textract_poc = TextractPOC()
    
    # Example usage with different image types
    document_types = [
        ('sample_id.jpg', 'id')
    ]
    
    for image_path, doc_type in document_types:
        if not os.path.exists(image_path):
            print(f"Warning: {image_path} not found. Skipping.")
            continue
        
        print(f"\n=== Processing {doc_type.upper()} Document: {image_path} ===")
        
        if doc_type == 'document':
            blocks = textract_poc.detect_document_text(image_path)
            textract_poc.visualize_document_geometry(image_path, blocks)
        
        elif doc_type == 'form':
            textract_poc.analyze_document(image_path)
        
        elif doc_type == 'id':
            textract_poc.analyze_id(image_path)

if __name__ == '__main__':
    main()
