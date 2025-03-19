import streamlit as st
import time
from zhipuai import ZhipuAI
import os
import zipfile
import tarfile
import tempfile
import chardet
import markdown
import git
from github import Github
import requests
import shutil
import subprocess
import os
from urllib.parse import urlparse
import shutil
import os


def metagpt_generate_code(instruction):
    command = ['metagpt', instruction]
    subprocess.run(command, capture_output=True, text=True)
    

def zip_and_remove_other_folder(workspace_dir, exclude_folder):
    current_dir = os.getcwd()
    workspace_path = os.path.join(current_dir, workspace_dir)

    if not os.path.exists(workspace_path):
        st.error(f"Table of Contents '{workspace_dir}' Not found.")
        return None

    folders = [
        f for f in os.listdir(workspace_path) 
        if os.path.isdir(os.path.join(workspace_path, f)) and f != exclude_folder
    ]
    print(folders)

    if not folders:
        st.error("文件不存在")
        return None

    # 找到最新创建的文件夹
    latest_folder = max(folders, key=lambda f: os.path.getctime(os.path.join(workspace_path, f)))
    folder_to_zip_path = os.path.join(workspace_path, latest_folder)

    output_zip_name = f"{latest_folder}.zip"
    output_path = os.path.join(current_dir, output_zip_name)

    shutil.make_archive(output_path[:-4], 'zip', folder_to_zip_path)
    shutil.rmtree(folder_to_zip_path)

    return output_path



def delete_zip_file(file_path):
    """下载后删除 ZIP 文件的函数"""
    if os.path.exists(file_path):
        os.remove(file_path)
        st.session_state.zip_file_path = None  # 清除状态中的文件路径
        st.success("ZIP 文件已删除。")
    
    

    workspace_dir = "workspace"
    current_dir = os.getcwd()
    workspace_path = os.path.join(current_dir, workspace_dir)

    if os.path.exists(workspace_path) and os.path.isdir(workspace_path):
        shutil.rmtree(workspace_path)
        print(f"目录 '{workspace_dir}' 已删除。")
    else:
        print(f"目录 '{workspace_dir}' 不存在。")




def zip_and_remove_unique_folder(workspace_dir):
    # 获取当前工作目录
    current_dir = os.getcwd()

    # 构建 workspace 目录的完整路径
    workspace_path = os.path.join(current_dir, workspace_dir)

    # 检查 workspace 目录是否存在
    if not os.path.exists(workspace_path):
        print(f"Table of Contents'{workspace_dir}' Not found.")
        return

    # 获取 workspace 目录下的所有文件夹
    folders = [f for f in os.listdir(workspace_path) if os.path.isdir(os.path.join(workspace_path, f))]

    # 检查是否存在唯一一个文件夹
    if len(folders) != 1:
        print("workspace The directory must contain only one folder and must not include anything else.")
        return

    # 获取唯一文件夹的名称
    unique_folder = folders[0]
    unique_folder_path = os.path.join(workspace_path, unique_folder)

    # 打包文件夹
    output_zip_name = f"{unique_folder}.zip"
    shutil.make_archive(os.path.join(current_dir, output_zip_name[:-4]), 'zip', unique_folder_path)

    # 删除文件夹
    shutil.rmtree(unique_folder_path)
    print(f"Directory '{unique_folder}' has been zipped as'{output_zip_name}' and removed.")
    return output_zip_name





zp_api_key = "a32529c7a9ec4c569f94610343daff6e.jTWpyMwM8DGIkAmz"

def read_file_encoding(file_path):
    # 检测文件编码
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']
    return encoding

def metagpt_generate_code(instruction):
    comand = ['metagpt', instruction, '--code-review', '--investment', '5', '--run-tests', '--n-round','6']
    result = subprocess.run(comand)



def get_repo_name(github_url):
    # 解析 URL，获取仓库路径
    parsed_url = urlparse(github_url)
    
    # 获取路径的最后一部分，即仓库名
    repo_name = os.path.basename(parsed_url.path)
    
    # 去掉.git后缀（如果有）
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]
    
    return repo_name

def chatbot_page():  
        st.title("💬 LLMSDH: Software Prototype Development Platform")
        st.caption("🚀 A Streamlit LLMSDH: Software Prototype Development Platform powered by Zhipu Chat")
        # Streamlit 代码



        prompt = st.text_input("Input Command：")
        if st.button("Generate Code and Package Files"):
    # 调用函数生成代码
               metagpt_generate_code(prompt)

           
               st.success("Code Generation Successful!")
        
              # 打包并删除 workspace 中的唯一文件夹（排除 'storage' 文件夹）
               zip_file_path = zip_and_remove_other_folder("workspace", "storage")
        
               if zip_file_path:
            # 在会话状态中存储 ZIP 文件路径
                   st.session_state.zip_file_path = zip_file_path
            
                     # 提供下载按钮
                   with open(zip_file_path, "rb") as f:
                          st.download_button(
                          label="Download zip Files",
                          data=f,
                                file_name=os.path.basename(zip_file_path),
                                mime="application/zip",
                                on_click=lambda: delete_zip_file(st.session_state.zip_file_path)  # 下载后删除文件
                            )
           

            

def CodeGeeXIntrepreting():  
    from  jsonformat import analyze_project_profile
    st.title("🦜🔗 LLMSDH: Software System Introduction Development Platform")  
    st.caption("🚀 A Streamlit LLMSDH: Software System Introduction Development Platform powered by Zhipu Chat")

    # 初始化会话状态
    if "codegeex_intrepreting_messages" not in st.session_state:
        st.session_state["codegeex_intrepreting_messages"] = []

    # 创建一个固定在顶部的消息显示区域
    message_placeholder = st.empty()

    if "code_update_projects" not in st.session_state:
        st.session_state["code_update_projects"] = []
    
    if "code_github_urls" not in st.session_state:
        st.session_state["code_github_urls"] = []

     # 创建一个固定在顶部的消息显示区域
    message_placeholder = st.empty()

    # 显示历史消息
    with message_placeholder.container():
        for message in st.session_state["codegeex_intrepreting_messages"]:
            if "project_name" in message:
                st.chat_message(message["role"]).write(f"{message['content']} (Project: {message['project_name']})")
            else:
                st.chat_message(message["role"]).write(message["content"])

    # GitHub 链接输入框
    github_url = st.text_input("Enter GitHub Project Link")

    # 上传文件或通过 GitHub 下载项目
    uploaded_project = st.file_uploader("Or upload project files", type=("zip", "tar", "tar.gz", "tar.bz2"), accept_multiple_files=True)
    
    # 检查 GitHub 链接是否为新的
    if github_url and github_url not in st.session_state["code_github_urls"]:
        st.session_state["code_github_urls"].append(github_url)  # 记录新的 GitHub 链接
        
        # 下载 GitHub 项目
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_dir = download_github_repo(github_url, temp_dir)
            if repo_dir:
                analyze_project_profile(repo_dir, message_placeholder, get_repo_name(github_url))

    if uploaded_project:
        # 仅对新上传的项目进行处理
        new_projects = [project for project in uploaded_project if project.name not in st.session_state["code_update_projects"]]
        
        for project in new_projects:
            with tempfile.TemporaryDirectory() as temp_dir:
                if project.name.endswith('.zip'):
                    with zipfile.ZipFile(project, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                elif project.name.endswith(('.tar', '.tar.gz', '.tar.bz2')):
                    with tarfile.open(project, 'r') as tar_ref:
                        tar_ref.extractall(temp_dir)
                analyze_project_profile(temp_dir, message_placeholder, project.name)




    


    
    
    





def SoftwareEngineerDefectDetection():
    st.title("📝 LLMSDH:Rapid Short Code Detection Platform")
    st.caption("🚀 A Streamlit LLMSDH: Rapid Short Code Detection Platform powered by  Zhipu Chat")
    
    # 初始化会话状态
    if "software_engineer_defect_detection_messages" not in st.session_state:
        st.session_state["software_engineer_defect_detection_messages"] = []
    
    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []

    # 创建一个固定在顶部的消息显示区域
    message_placeholder = st.empty()

    # 显示历史消息
    with message_placeholder.container():
        for message in st.session_state["software_engineer_defect_detection_messages"]:
            if "file_name" in message:
                st.chat_message(message["role"]).write(f"{message['content']} (from file: {message['file_name']})")
            else:
                st.chat_message(message["role"]).write(message["content"])

    # 创建一个固定在底部的输入模块
    with st.container():
        st.write("### Upload Code Files and Ask Questions")
        uploaded_files = st.file_uploader("Please upload the code files.", type=("py", "cpp", "java", "c", "go", "js", "ts", "html", "css", "scss"), accept_multiple_files=True)
        

    if uploaded_files:
        # 仅对新上传的文件进行处理
        new_files = [file for file in uploaded_files if file.name not in st.session_state["uploaded_files"]]
        
        for file in new_files:
            code = file.read().decode()
            prompt = f"""Please detect code defects in the code file and provide a detailed explanation. Return the total number of defects and defect types. Evaluate the overall code quality. Additionally, for each defect, provide the location in the file, the defective code, the corrected code, and the reason for the correction.\n\nCode file name：{file.name}\n\nThis is the code file.:\n\n<code>{code}\n\n</code>\n\n"""

            client = ZhipuAI(api_key=zp_api_key)
            response = client.chat.completions.create(
                model="glm-4-plus",  
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )

            msg = response.choices[0].message.content

            # 更新显示区以显示新消息
            with message_placeholder.container():
                for message in st.session_state["software_engineer_defect_detection_messages"]:
                    if "file_name" in message:
                        st.chat_message(message["role"]).write(f"{message['content']} (来自文件: {message['file_name']})")
                    else:
                        st.chat_message(message["role"]).write(message["content"])
            
                typing_placeholder = st.empty()
                full_msg = ""
                for char in msg:
                    full_msg += char
                    typing_placeholder.chat_message("assistant").write(full_msg)
                    time.sleep(0.05)
                    
                typing_placeholder.chat_message("assistant").write(msg)
                st.session_state["software_engineer_defect_detection_messages"].append({"role": "assistant", "content": msg, "file_name": file.name})

                # 记录已上传的文件
                st.session_state["uploaded_files"].append(file.name)

                # 生成 Markdown 文件内容
                markdown_content = f"# Code Defect Detection Report\n\n## filename: {file.name}\n\n{msg}"

                # 提供下载按钮
                st.download_button(
                    label="Download Report",
                    data=markdown_content,
                    file_name=f"{file.name}_defect_report.md",
                    mime="text/markdown"
                )
                






# 下载 GitHub 项目函数
def download_github_repo(github_url, temp_dir):
    try:
        repo_name = github_url.split('/')[-1]
        repo_dir = os.path.join(temp_dir, repo_name)

        # 克隆 GitHub 仓库到临时目录
        git.Repo.clone_from(github_url, repo_dir)
        return repo_dir
    except Exception as e:
        st.error(f"Unable to download the project: {str(e)}")
        return None

async def SoftwareProjectEvaluation():
    st.title("🔎 LLMSDH: Software Defect Detection Platform")
    st.caption("🚀 A Streamlit LLMSDH: Software Defect Detection Platform powered by Zhipu Chat")

    # 初始化会话状态
    if "software_project_evaluation_messages" not in st.session_state:
        st.session_state["software_project_evaluation_messages"] = []
    
    if "uploaded_project" not in st.session_state:
        st.session_state["uploaded_project"] = []

    if "github_urls" not in st.session_state:
        st.session_state["github_urls"] = []
        
    # 创建一个固定在顶部的消息显示区域
    message_placeholder = st.empty()

    # 显示历史消息
    with message_placeholder.container():
        for message in st.session_state["software_project_evaluation_messages"]:
            if "project_name" in message:
                st.chat_message(message["role"]).write(f"{message['content']} (From the projec: {message['project_name']})")
            else:
                st.chat_message(message["role"]).write(message["content"])

    # GitHub 链接输入框
    github_url = st.text_input("Enter GitHub Project Link")

    # 上传文件或通过 GitHub 下载项目
    uploaded_project = st.file_uploader("Or upload project files.", type=("zip", "tar", "tar.gz", "tar.bz2"), accept_multiple_files=True)
    
    # 检查 GitHub 链接是否为新的
    if github_url and github_url not in st.session_state["github_urls"]:
        st.session_state["github_urls"].append(github_url)  # 记录新的 GitHub 链接
        
        # 下载 GitHub 项目
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_dir = download_github_repo(github_url, temp_dir)
            if repo_dir:
                await  analyze_project_async(repo_dir, message_placeholder, get_repo_name(github_url))

    if uploaded_project:
        # 仅对新上传的项目进行处理
        new_projects = [project for project in uploaded_project if project.name not in st.session_state["uploaded_project"]]
        
        for project in new_projects:
            with tempfile.TemporaryDirectory() as temp_dir:
                if project.name.endswith('.zip'):
                    with zipfile.ZipFile(project, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                elif project.name.endswith(('.tar', '.tar.gz', '.tar.bz2')):
                    with tarfile.open(project, 'r') as tar_ref:
                        tar_ref.extractall(temp_dir)
                await analyze_project_async(temp_dir, message_placeholder, project.name)

# 处理项目的代码文件并评测
def analyze_project(project_dir, message_placeholder, name):
    # 识别代码文件
    code_files = []
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(('.py', '.cpp', '.java', '.c', '.go','.rs', '.ipynb')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding=read_file_encoding(file_path), errors='ignore') as f:
                    code_content = f.read()
                file_path = os.path.relpath(os.path.join(root, file), project_dir)
                code_files.append((file, file_path, code_content))
    
    prompts = ["This is a software project under development. I will provide the names, paths, and contents of all the code files in the project. Please review each code file, checking only for null pointer issues, memory leaks, concurrency errors, and arithmetic or logical errors. Provide detailed explanations and evaluate the quality of the code. Ignore any irrelevant contextual information and perform defect analysis based on the project code.\n\n"]
    
    for file_name, file_path, code_content in code_files:
        prompt = f"""This is the name of the code file. {file_name} ,The path of the code file is. {file_path}.Combine with other code files to perform defect analysis. The code content is as follows:\n\n<code>{code_content}\n\n</code> Only check for null pointer issues, memory leaks, concurrency errors, and arithmetic or logical errors. Provide detailed explanations, identify the defects in the code file, and for each defect, give the corrective measures and the cause of the error. Ignore irrelevant contextual information. Locate the defect in the code context and provide the fixed code.\n\n"""
        prompts .append(prompt)

    prompts.append("Please summarize the strengths and weaknesses of the project, fix the defects in each file, and provide detailed explanations along with the fixed code.")
    
   
    msgs = ""
    client = ZhipuAI(api_key=zp_api_key)
    messages = []
    for prompt in prompts:
       
        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
        model="glm-4-flash",  
        messages=messages,
    )
        message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": message})
        print(message)
        msgs += message + "\n\n"
    

    prompt = "Please evaluate the project's code quality and provide a project summary."
    response = client.chat.completions.create(
        model="glm-4-flash",  
        messages=messages,
    )
    

    msg = response.choices[0].message.content

    msgs += msg + "\n\n"
    
    with message_placeholder.container():
                    for message in st.session_state["software_project_evaluation_messages"]:
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
                    st.session_state["software_project_evaluation_messages"].append({"role": "assistant", "content": msg, "project_name":name})

                    # 记录已上传的项目
                    st.session_state["uploaded_project"].append(name)

                    # 生成 Markdown 文件内容
                    markdown_content = f"# Project Evaluation Report\n\n## Project Name: {name}\n\n{msgs}"

                    # 提供下载按钮
                    st.download_button(
                        label="Download Report",
                        data=markdown_content,
                        file_name=f"{name}_project_report.md",
                        mime="text/markdown"
                    )


import asyncio
import aiohttp
from zhipuai import ZhipuAI



async def analyze_project_async(project_dir, message_placeholder, name):
    from zp import process_chunked_prompts, fetch_response
    # 识别代码文件（保持不变）
    code_files = []
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(('.py', '.cpp', '.java', '.c', '.go', '.rs', '.ipynb')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding=read_file_encoding(file_path), errors='ignore') as f:
                    code_content = f.read()
                file_path = os.path.relpath(os.path.join(root, file), project_dir)
                code_files.append((file, file_path, code_content))

    
    prompts = []
    for file_name, file_path, code_content in code_files:
        prompt = f"""This is the name of the code file. {file_name} ,The path of the code file is. {file_path},Perform defect analysis by combining with the code files. The code content is as follows:\n\n<code>{code_content}\n\n</code>Only check for null pointer issues, memory leaks, concurrency errors, and arithmetic or logical errors. Provide detailed explanations, identify the defects in the code file, and for each defect, give the corrective measures and the cause of the error. Ignore irrelevant contextual information. Locate each defect in the code context and provide the fixed code. The format of the response should be: "This is the defect detection report for the xxx code file."\n\n"""
        prompts.append(prompt)

    
    
    msgs = ""
    client = ZhipuAI(api_key=zp_api_key)
    
    
    # 等待所有任务完成
    responses, messages = await process_chunked_prompts(prompts=prompts, api_key=zp_api_key)
    
    # 处理每个响应
    for message in responses:
        msgs += message + "\n\n"

    # 最后总结项目的代码质量
   
    final_response= "For the project{} defect detection for the project was successful!!!".format(name)

    # 显示评估结果
    with message_placeholder.container():
        for message in st.session_state["software_project_evaluation_messages"]:
            if "project_name" in message:
                st.chat_message(message["role"]).write(f"{message['content']} (From the project: {message['project_name']})")
            else:
                st.chat_message(message["role"]).write(message["content"])
        
        typing_placeholder = st.empty()
        full_msg = ""
        for char in final_response:
            full_msg += char
            typing_placeholder.chat_message("assistant").write(full_msg)
            await asyncio.sleep(0.05)  # 异步等待
        typing_placeholder.chat_message("assistant").write(final_response)
        st.session_state["software_project_evaluation_messages"].append({"role": "assistant", "content": final_response, "project_name": name})

        # 记录已上传的项目
        st.session_state["uploaded_project"].append(name)

        # 生成 Markdown 文件内容
        markdown_content = f"# Project Evaluation Report\n\n## Project Name: {name}\n\n{msgs}"

        # 提供下载按钮
        st.download_button(
            label="Download Markdown Report",
            data=markdown_content,
            file_name=f"{name}_project_report.md",
            mime="text/markdown"
        )






def main():  
    if "current_page" not in st.session_state:  
        st.session_state.current_page = "home"  
  
    st.sidebar.title("LLMSDH: Large Model Assistance in Software Development")  
    if st.sidebar.button("💬 LLMSDH: Software Prototype Development Platform"):  
        st.session_state.current_page = "chatbot"  
    if st.sidebar.button("🦜🔗 LLMSDH: Software System Introduction Development Platform"):  
        st.session_state.current_page = "codegeex"  
    if st.sidebar.button("📝 LLMSDH: Rapid Short Code Detection Platform"):  
        st.session_state.current_page = "Software Engineer Defect Detection"  
    
    if st.sidebar.button("🔎LLMSDH: Software Defect Detection Platform"):
        st.session_state.current_page = "Software Project Evaluation"  
        


    if st.session_state.current_page == "chatbot":  
        chatbot_page()  
    elif st.session_state.current_page == "codegeex":  
        CodeGeeXIntrepreting()  
    elif st.session_state.current_page == "Software Engineer Defect Detection":  
        SoftwareEngineerDefectDetection()  
    elif st.session_state.current_page == "Software Project Evaluation":  
        asyncio.run(SoftwareProjectEvaluation())  
        
  
if __name__ == "__main__":  
    main()
