import base64
import hashlib
import json
import os
from typing import List, Dict

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

import config
from comidp_exception import IDPException, ERROR_CODES
from comidp_tools_controller import api_idp_data_extract_post, api_idp_data_extract_post_with_data

mcp = FastMCP("ComIDP Tool", on_tool_error="raise")
load_dotenv()
config.IDPKEY = os.getenv("IDPKEY", "")

from pathlib import Path
import os

SUPPORTED_EXTS = [".pdf"]


def get_supported_files(folder: str, recursive: bool = False) -> list:
    folder_path = Path(folder)
    pattern_prefix = "**/" if recursive else ""
    files = []

    for ext in SUPPORTED_EXTS:
        pattern = f"{pattern_prefix}*{ext}"
        files.extend([f.resolve() for f in folder_path.glob(pattern) if f.is_file()])

    return files


@mcp.tool(
    name="data_extraction_from_folder",
    description="""
    Extract data from PDF files in a folder and save to TXT files in the specified folder.

    Params:
        folder: Path to the folder containing PDF files.
        save_dir_path: Path to the folder where the result files will be saved.
        key: The API key for IDPKEY. Required on the first call.
        recursive: If true, recursively search subdirectories for PDF files.
        err_msg_lang: Optional language code for error messages (e.g., 'zh' or 'en'). Defaults to 'en'.

        Returns:
        A dictionary mapping each input file path to its corresponding output TXT file path.
        If an error occurs, the value will be an error message.
    """
)
def data_extraction_from_folder(folder: str, save_dir_path: str, recursive: bool = False, key: str = "",
                                err_msg_lang: str = "en") -> Dict[str, str]:
    if not os.path.exists(folder):
        raise IDPException(*ERROR_CODES["FILE_NOT_FOUND"], err_msg_lang)

    pdf_files = get_supported_files(folder, recursive)
    if not pdf_files:
        raise IDPException(*ERROR_CODES["FILE_NOT_FOUND"], err_msg_lang)

    return data_extraction(pdf_files, save_dir_path, key, err_msg_lang)


@mcp.tool(
    name="data_extraction",
    description="""
    Extract data from PDF files and save to TXT files in the specified folder.

    Params:
        filenames: A list of PDF file paths.
        save_dir_path: Folder where the result TXT files will be saved.
        key: The API key for IDPKEY. Required on the first call.
        err_msg_lang: Optional language code for error messages (e.g., 'zh' or 'en'). Defaults to 'en'.

    Returns:
        A dictionary mapping each input file path to its corresponding output TXT file path.
        If an error occurs, the value will be an error message.
    """
)
def data_extraction(filenames: list, save_dir_path: str = "output", key: str = "", err_msg_lang: str = "en") -> Dict[
    str, str]:
    if key:
        config.IDPKEY = key
    if not config.IDPKEY:
        raise IDPException(*ERROR_CODES["INVALID_KEY"], err_msg_lang)

    if not os.path.exists(save_dir_path):
        os.makedirs(save_dir_path)
    save_dir_path = os.path.abspath(save_dir_path)

    generated_files = []

    for file_path in filenames:
        if not os.path.exists(file_path):
            raise IDPException(*ERROR_CODES["FILE_NOT_FOUND"], err_msg_lang)

        result = api_idp_data_extract_post(file_path)
        json_result = json.loads(result)

        if str(json_result.get("code")) != "200":
            error_code = str(json_result.get("code"))
            error_msg = json_result.get("msg",
                                        ERROR_CODES["EXTRACTION_FAILED"][1].get(err_msg_lang, "Extraction failed"))
            raise IDPException(error_code, {"en": error_msg, "zh": error_msg}, err_msg_lang)

        data = json_result.get("data", "")
        data_str = json.dumps(data, ensure_ascii=False, indent=2) if isinstance(data, dict) else str(data)

        base_name = os.path.splitext(os.path.basename(file_path))[0]
        target_path = os.path.join(save_dir_path, base_name + ".txt")

        counter = 1
        while os.path.exists(target_path):
            target_path = os.path.join(save_dir_path, f"{base_name}_{counter}.txt")
            counter += 1

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(data_str)

        generated_files.append(os.path.basename(target_path))

    return {
        "status": "success",
        "saved_files": generated_files,
        "save_dir": save_dir_path
    }


if __name__ == "__main__":
    try:
        mcp.run()

    except Exception as e:
        print("❌ MCP startup failed:", e)