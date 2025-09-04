from typing import List, Union
from paddlex import create_pipeline
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document






class ImageOCRReader(BaseReader):
    """Extract text from images using PP-OCR v5 and return Document objects"""
    
    def __init__(self, lang='en', use_gpu=False, model='PP-OCRv5_server_det', **kwargs):
        """
        Args:
            lang: OCR language ('ch', 'en', 'fr', etc.)
            use_gpu: Whether to use GPU acceleration
            **kwargs: Other parameters passed to PaddleOCR
        """
        device = "gpu" if use_gpu else "cpu"
        self.lang = lang
        self.ocr = create_pipeline(
            pipeline="OCR",
            text_detection_model_name=model,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            lang=lang,
            device=device
        )

    
    def load_data(self, file: Union[str, List[str]]) -> List[Document]:
        """
        Extract text from single or multiple image files, return Document list
        
        Args:
            file: Image path string or list of paths
            
        Returns:
            List[Document]: List of Document objects with extracted text and metadata
        """
        results = self.ocr.predict(input=file)
        documents = []
        
        for result in results:
            # Extract text from OCR results
            if 'rec_texts' in result and result['rec_texts']:
                extracted_text = ' '.join(result['rec_texts'])
            else:
                extracted_text = ""
            
            # Calculate average confidence
            if 'rec_scores' in result and result['rec_scores']:
                avg_confidence = sum(result['rec_scores']) / len(result['rec_scores'])
            else:
                avg_confidence = 0.0
            
            # Create Document with metadata
            doc = Document(
                text=extracted_text,
                metadata={
                    "image_path": result.get('input_path', str(file)),
                    "ocr_model": "PP-OCRv5",
                    "language": self.lang,
                    "num_text_blocks": len(result.get('rec_texts', [])),
                    "avg_confidence": round(avg_confidence, 4)
                }
            )
            documents.append(doc)
        
        return documents
        