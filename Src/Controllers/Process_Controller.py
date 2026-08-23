from Controllers.Base_Controller import Base_controller
from Controllers.Project_Controller import Project_Controller
from langchain_community.document_loaders import TextLoader
# from langchain_community.document_loaders import PyMuPdfLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from docling.document_converter import DocumentConverter, PdfFormatOption, InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling_core.types.doc import TextItem, TableItem, PictureItem
from langchain_core.documents import Document

import os

class Process_Controller(Base_controller):
    def __init__(self):
        super().__init__()
        pipeline_options = PdfPipelineOptions()
        pipeline_options.generate_picture_images = True

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options
                )
            }
        )

    def get_file_ext(self,file_id:str):
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self,file_id:str,project_id:str):
        file_ext = self.get_file_ext(file_id=file_id)
        file_path =os.path.join(
        Project_Controller().get_uploaded_file_path(project_id=project_id),
        file_id 
        )

        if file_ext == ".txt":
            return TextLoader(file_path,encoding ="utf-8")
        

        if file_ext in [".pdf", ".docx", ".pptx"]:
            result = self.converter.convert(file_path)

            print("Pictures:", len(result.document.pictures))
            print("Tables:", len(result.document.tables))

            return result
        
        return None

    def get_file_content(self,file_id:str,project_id:str):
        load_data = self.get_file_loader(file_id=file_id,project_id = project_id)
        if load_data:

            if self.get_file_ext(file_id) == ".txt":
                return load_data.load()

            return load_data.document

        return None


    def extract_document_elements(self, document):

        elements = []

        for item, level in document.iterate_items():

            if isinstance(item, TextItem):

                elements.append({
                    "type": "text",
                    "content": item.text,
                    "level": level
                })

            elif isinstance(item, TableItem):

                table = item.export_to_markdown(
                    doc=document
                )

                elements.append({
                    "type": "table",
                    "content": table,
                    "level": level
                })

            elif isinstance(item, PictureItem):

                image = item.get_image(document)

                elements.append({
                    "type": "picture",
                    "content": image,
                    "level": level
                })

        return elements
    
    def process_file_content(self,file_content:list,chunk_size=500,overlap_size=20):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = overlap_size,
            length_function = len
        )
        
        if isinstance(file_content, list):
            return text_splitter.split_documents(file_content)

        elements = self.extract_document_elements(
            file_content
        )

        documents = []

        for element in elements:

            if element["type"] == "text":

                documents.append(
                    Document(
                        page_content=element["content"],
                        metadata={
                            "content_type": "text"
                        }
                    )
                )

            elif element["type"] == "table":

                documents.append(
                    Document(
                        page_content=element["content"],
                        metadata={
                            "content_type": "table"
                        }
                    )
                )

            elif element["type"] == "picture":

                pass

        return text_splitter.split_documents(documents)
