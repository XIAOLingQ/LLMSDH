source /etc/network_turbo
git clone https://github.com/XIAOLingQ/LLMSDH.git
cd LLMSDH

pip install zhipu streamlit metagpt pygithub
pip install --upgrade cryptography pyOpenSSL


streamlit run zhipupower.py