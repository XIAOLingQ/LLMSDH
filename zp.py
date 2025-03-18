import asyncio
import aiohttp
import json
from tqdm.asyncio import tqdm
# 将prompts按每30个一组分块
def chunked_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


async def fetch_response(api_key, model, messages, prompt):
    url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": model,
        "messages": messages
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            result = await response.json()
            
            
            if 'choices' in result and result['choices']:
                # 获取响应内容并追加到messages
                content = result['choices'][0]['message']['content']
                messages.append({"role": "assistant", "content": content})
                # 返回响应内容以及最近的两条消息
                return content, messages[-2:]
            else:
                # 处理没有 "choices" 键或响应为空的情况 
                messages.append({"role": "assistant", "content": "对不起，我没有理解你的意思。"})
                return "对不起，我没有理解你的意思。", messages[-2:]


# 执行块中的任务
async def process_chunked_prompts(prompts, api_key):
    all_responses = []
    
    messages = [{"role": "user", "content": "这是一个开发完成的项目，请你对代码文件进行缺陷检测， 仅仅检测空指针，内存泄漏，并发错误，算术逻辑错误。并给出详细的解释。找出代码文件的缺陷。对每个缺陷，给出修复措施和错误原因，忽略无关的上下文信息。对每个缺陷进行代码上下文的定位，并给出修复后的代码。"}]
    # 分块
    for chunk in tqdm(chunked_list(prompts, 31), desc="Code Defect Detection"):
        tasks = []
        
        
        # 创建任务列表
        for prompt in chunk:
            message = messages.copy()
            message.append({"role": "user", "content": prompt})
            tasks.append(fetch_response(api_key=api_key, model="glm-4-flash", messages=message, prompt=prompt))

         # 等待当前块中的任务完成
        task_results = await asyncio.gather(*tasks)
        
        for response, message in task_results:
            
            
            # 收集所有的响应
            all_responses.append(response)
            messages.extend(message)
        
        


    return all_responses, messages