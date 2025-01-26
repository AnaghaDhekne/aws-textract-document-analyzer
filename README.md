# aws-textract-document-analyzer

AWS Textractor document analyzer is a Python-based tool that leverages AWS Textract to analyze and extract text from images and documents. This tool supports text extraction, form and table analysis, ID document analysis, and visualization of detected text blocks with bounding boxes.

## Features
- **Text Detection:** Extracts text from document images.
- **Form and Table Analysis:** Identifies key-value pairs and table structures in documents.
- **ID Document Analysis:** Extracts information from identity documents like passports or driver's licenses.
- **Visualization:** Generates an image with bounding boxes around detected text blocks.

## Requirements
- Python 3.6+
- AWS CLI configured with valid credentials
- Required Python libraries:
  - `boto3`
  - `Pillow`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/AnaghaDhekne/aws-textract-document-analyzer.git
   cd aws-textract-document-analyzer
   ```

2. Install dependencies:
   ```bash
   pip install boto3 Pillow
   ```

3. Configure AWS credentials using the AWS CLI or environment variables:
   ```bash
   aws configure
   ```

   Alternatively, set the environment variables directly:
   ```bash
   export AWS_ACCESS_KEY_ID=<your-access-key>
   export AWS_SECRET_ACCESS_KEY=<your-secret-key>
   export AWS_DEFAULT_REGION=<your-region>
   ```

## Usage
1. Place the document images you want to process in the working directory.
2. Run the script:
   ```bash
   python textract_poc.py
   ```

3. The script will process the specified document types (e.g., ID documents, forms) and display the extracted information in the console.

## Code Structure
### `TextractPOC` Class
- **`__init__()`**: Initializes the Textract client.
- **`detect_document_text(image_path)`**: Detects text in a document image.
- **`analyze_document(image_path)`**: Analyzes forms and tables in a document image.
- **`analyze_id(image_path)`**: Analyzes ID documents to extract key information.
- **`visualize_document_geometry(image_path, blocks)`**: Visualizes detected text blocks by drawing bounding boxes on the original image.

### `main()` Function
- Initializes the `TextractPOC` class and processes predefined document types (e.g., ID documents, forms).
- Example usage is provided for processing a sample ID document (`sample_id.jpg`).

## Output
- Extracted text and analysis results are displayed in the console.
- Visualized output with bounding boxes is saved as `textract_geometry_visualization.jpg`.

## Example
To process a sample ID document:
1. Ensure the file `sample_id.jpg` exists in the working directory.
2. Run the script:
   ```bash
   python textract_poc.py
   ```
3. Results will include extracted text and any detected key-value pairs or table data.

## Notes
- Ensure your AWS Textract service permissions are configured correctly to avoid access errors.
- Update `document_types` in the `main()` function to add or modify document types and file paths.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
