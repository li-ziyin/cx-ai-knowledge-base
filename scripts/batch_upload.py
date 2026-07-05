import os
import requests

BASE_URL = "http://localhost:8000"


def upload_file(filepath):
    """上传单个文件"""
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        files = {"file": (filename, f, "text/plain")}
        response = requests.post(f"{BASE_URL}/api/documents/upload", files=files)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {filename}: 新增 {data['chunks_added']} 个片段")
        else:
            print(f"❌ {filename}: 失败 {response.status_code}")


def batch_upload(folder_path="./data/uploads"):
    """批量上传文件夹内所有文档"""
    if not os.path.exists(folder_path):
        print(f"文件夹不存在: {folder_path}")
        return

    files = [f for f in os.listdir(folder_path)
             if f.endswith((".txt", ".pdf", ".docx"))]

    print(f"发现 {len(files)} 个文件，开始上传...")
    for filename in files:
        upload_file(os.path.join(folder_path, filename))
    print("批量上传完成！")


if __name__ == "__main__":
    import sys

    folder = sys.argv[1] if len(sys.argv) > 1 else "./data/uploads"
    batch_upload(folder)