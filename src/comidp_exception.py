SUPPORTED_LANGS = {"en", "zh"}

class IDPException(Exception):
    def __init__(self, code, messages: dict, lang: str = "en"):
        if lang not in SUPPORTED_LANGS:
            lang = "en"
        message = messages.get(lang, messages.get("en", "Unknown error"))
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


ERROR_CODES = {
    "INVALID_KEY": ("400", {"zh": "序列码认证错误（或序列码无效）", "en": "Invalid API key"}),
    "UPLOAD_FAILED": ("01003", {"zh": "上传文件失败", "en": "Upload failed"}),
    "DOWNLOAD_FAILED": ("01004", {"zh": "下载文件失败", "en": "Download failed"}),
    "FILE_NOT_FOUND": ("01203", {"zh": "找不到或无法打开文件", "en": "File not found or cannot be opened"}),
    "NO_ASSET": ("05002", {"zh": "资产不足", "en": "Insufficient assets"}),
    "ENCRYPTED_DOC": ("02201", {"zh": "文档已加密", "en": "Document is encrypted"}),
    "BROKEN_DOC": ("02203", {"zh": "文档异常（或文档破损）", "en": "Corrupted or broken document"}),
    "UNSUPPORTED_FORMAT": ("02204", {"zh": "不支持的文件格式（仅支持 PDF）", "en": "Unsupported file format (PDF only)"}),
    "UNKNOWN_ERROR": ("01202", {"zh": "未知错误", "en": "Unknown error"}),
    "EMPTY_FILE": ("04002", {"zh": "文件大小为零，您的文件中没有内容", "en": "File is empty, no content detected"}),
    "FIELD_MISSING": ("06001", {"zh": "抽取字段不存在", "en": "Field not found"}),
    "EXTRACTION_FAILED": ("06002", {"zh": "抽取失败", "en": "Extraction failed"}),
    "NETWORK_ERROR": ("06003", {"zh": "网络错误", "en": "Network error"}),
    "PAGE_OVERFLOW": ("06004", {"zh": "指定抽取页码超出文档最大页码数", "en": "Specified page exceeds document length"}),
    "PAGE_COUNT_EXCEED": ("06005", {"zh": "指定抽取文档页面数超出最大值50", "en": "Exceeded max page count (50)"})
}

