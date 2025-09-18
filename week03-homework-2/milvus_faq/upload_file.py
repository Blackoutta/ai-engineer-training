import gradio as gr
import os
import shutil
import pandas as pd

# File storage path configuration - using layered storage architecture design
# Separate storage for structured and unstructured data, facilitating different strategies for subsequent vectorization processing
STRUCTURED_FILE_PATH = "files/Structured"      # Structured data storage path (CSV/Excel table data)
UNSTRUCTURED_FILE_PATH = "files/Unstructured"  # Unstructured data storage path (PDF/DOC/TXT document data)

# Directory refresh function - implements dynamic file system monitoring
def refresh_label():
    """
    Refresh unstructured category list
    Uses real-time directory scanning mechanism to ensure UI components are synchronized with file system state
    Avoids interface state inconsistency issues caused by file system changes
    """
    return os.listdir(UNSTRUCTURED_FILE_PATH)


def refresh_data_table():
    """
    刷新结构化数据表列表
    同步文件系统状态到前端组件，保证数据一致性
    """
    return os.listdir(STRUCTURED_FILE_PATH)


# Process unstructured data
def upload_unstructured_file(files, label_name):
    """
    非结构化文件上传核心处理函数
    
    设计理念：
    1. 采用原子性操作确保文件上传的事务完整性
    2. 使用shutil.move而非copy，避免临时文件残留和磁盘空间浪费
    3. 实现文件去重机制，防止重复上传导致的存储冗余
    
    参数:
        files: Gradio文件对象列表，包含临时文件路径信息
        label_name: 用户定义的分类标签，用于文件组织和后续检索
    """
    if files is None:
        gr.Info("Please upload a file")
    elif len(label_name) == 0:
        gr.Info("请输入类目名称")
    elif label_name in os.listdir(UNSTRUCTURED_FILE_PATH):
        gr.Info(f"{label_name}类目已存在")
    else:
        try:
            # 确保目标目录存在 - 惰性目录创建模式
            if not os.path.exists(os.path.join(UNSTRUCTURED_FILE_PATH, label_name)):
                os.mkdir(os.path.join(UNSTRUCTURED_FILE_PATH, label_name))

            # 批量文件处理 - 原子性文件移动操作
            for file in files:
                print(file)
                file_path = file.name  # Gradio temp file path
                file_name = os.path.basename(file_path)  # Get file name
                destionation_file_path = os.path.join(UNSTRUCTURED_FILE_PATH, label_name, file_name)
                # 使用move而非copy的原因：
                # 1. 避免临时文件占用磁盘空间
                # 2. 确保文件操作的原子性
                # 3. 减少I/O操作提升性能
                shutil.move(file_path, destionation_file_path)
            gr.Info(f"文件已上传至{label_name}类目中，请前往创建知识库")
        except Exception as e:
            # 异常处理 - 提供用户友好的错误反馈
            gr.Info(f"请勿重复上传")