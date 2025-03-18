import requests
import zipfile
import os
import json
import shutil
from zhipupower import ZhipuAI
from zhipupower import zp_api_key
import streamlit as st
import time
from zhipupower import read_file_encoding

def download_github_repo_as_zip(repo_url, extract_to="github"):
    """
    下载 GitHub 项目的 ZIP 压缩包并解压到指定目录
    :param repo_url: GitHub 仓库的 URL
    :param extract_to: 解压的目标文件夹
    """
    # 将仓库 URL 转换为下载 ZIP 文件的 URL
    if repo_url.endswith('.git'):
        repo_url = repo_url[:-4]
    zip_url = f"{repo_url}/archive/refs/heads/main.zip"

    # 获取 ZIP 文件
    response = requests.get(zip_url)
    if response.status_code == 200:
        # 创建下载目录
        os.makedirs(extract_to, exist_ok=True)
        
        # 保存 ZIP 文件
        zip_filename = os.path.join(extract_to, "repo.zip")
        with open(zip_filename, 'wb') as f:
            f.write(response.content)

        # 解压 ZIP 文件
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        # 删除 ZIP 文件
        os.remove(zip_filename)
        print(f"项目已成功下载并解压到 '{extract_to}' 文件夹")
    else:
        print(f"下载 ZIP 失败，状态码：{response.status_code}")

def get_directory_structure(root_dir):
    """
    获取文件夹的层级结构，并返回为字典格式
    :param root_dir: 文件夹的根路径
    :return: 文件夹结构的字典表示
    """
    structure = {}

    # 遍历文件夹及其子文件夹
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 获取相对于根目录的相对路径
        relative_path = os.path.relpath(dirpath, root_dir)
        if relative_path == '.':
            relative_path = ''

        # 根据相对路径构建嵌套字典结构
        folder_structure = structure
        if relative_path:
            for part in relative_path.split(os.sep):
                folder_structure = folder_structure.setdefault(part, {})

        # 将文件添加到相应的目录结构中
        folder_structure['files'] = filenames

    return structure

def save_structure_as_json(structure, output_file):
    """
    将字典格式的文件结构保存为 JSON 文件
    :param structure: 文件结构的字典
    :param output_file: 输出的 JSON 文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structure, f, ensure_ascii=False, indent=4)
    print(f"目录结构已保存为 {output_file}")



def clean_up_folder(folder):
    """
    删除指定的文件夹
    :param folder: 需要删除的文件夹路径
    """
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"已删除文件夹: {folder}")
    else:
        print(f"文件夹 {folder} 不存在")

def get_github_repo_structure(repo_url):
    # 替换为你想下载的 GitHub 仓库地址
    
    download_folder = "github"  # 解压到当前目录下的 'github' 文件夹
    
    # 下载并解压 GitHub 仓库
    download_github_repo_as_zip(repo_url, download_folder)

    # 获取解压后的根目录
    extracted_root = os.path.join(download_folder, os.listdir(download_folder)[0])

    # 获取解压后的文件夹结构
    directory_structure = get_directory_structure(extracted_root)

    

    
    
    clean_up_folder(download_folder)  # 删除下载的文件夹
    
    return directory_structure



# 处理项目的代码文件并评测
def analyze_project_profile(project_dir, message_placeholder, name):
    # 识别代码文件
    code_files = []
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(('.md')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding=read_file_encoding(file_path), errors='ignore') as f:
                    code_content = f.read()
                file_path = os.path.relpath(os.path.join(root, file), project_dir)
                code_files.append((file, file_path, code_content))
    
    prompts = "This is a completed software project. I will provide you with the project's readme.md file. Please analyze the project and write a project introduction, including details about the related tech stack and its advantages.\n\n"
    
    for file_name, file_path, code_content in code_files:
        prompt = f"""This is the name of the documentation file. {file_name} ，The path of the documentation file is.{file_path}。：\n\n<details>{code_content}\n\n</details> 。\n\n"""
        prompts +=(prompt)

    prompts +="Please provide me with a detailed documentation report, introducing the project's related tech stack, advantages, and design approach."
    
   
    msgs = ""
    client = ZhipuAI(api_key=zp_api_key)
    

   
    response = client.chat.completions.create(
        model="glm-4-plus",  
        messages=[{"role": "user", "content": prompts}],
    )
    

    msg = response.choices[0].message.content

    msgs += msg + "\n\n"
    
    with message_placeholder.container():
                    for message in st.session_state["codegeex_intrepreting_messages"]:
                        if "project_name" in message:
                            st.chat_message(message["role"]).write(f"{message['content']} (来自项目: {message['project_name']})")
                        else:
                            st.chat_message(message["role"]).write(message["content"])
                
                    typing_placeholder = st.empty()
                    full_msg = ""
                    for char in msg:
                        full_msg += char
                        typing_placeholder.chat_message("assistant").write(full_msg)
                        time.sleep(0.05)
                        
                    typing_placeholder.chat_message("assistant").write(msg)
                    st.session_state["codegeex_intrepreting_messages"].append({"role": "assistant", "content": msg, "project_name":name})

                    # 记录已上传的项目
                    st.session_state["code_update_projects"].append(name)

                    # 生成 Markdown 文件内容
                    markdown_content = f"# Project Analysis Report\n\n## Project Name: {name}\n\n{msgs}"

                    # 提供下载按钮
                    st.download_button(
                        label="Download Markdown Report",
                        data=markdown_content,
                        file_name=f"{name}_project_report.md",
                        mime="text/markdown"
                    )

