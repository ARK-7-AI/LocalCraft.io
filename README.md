# Localcraft.io 🛡️💼
**Privacy-First Career Automation: Local Compute, Absolute Data Sovereignty.**

Localcraft.io is a "Privacy-by-Design" suite built to solve the repetitive friction of the modern job search. By bridging the gap between browser-based job boards and local AI inference, it automates the creation of highly customized cover letters without your resume or PII ever leaving your hardware.

---

## 🚀 The Inspiration
As **MSAI students**, we spent hours manually tailoring cover letters. We realized that while AI is the solution, most tools demand you upload your life story to the cloud. We built Localcraft.io because **simple tools go a long way in solving everyday problems**, and your career data shouldn't be the price of admission.

## ✨ What it Does
1.  **Extract:** A lightweight browser plugin scrapes Job Descriptions (JDs) directly from job boards.
2.  **Transmit:** Data is securely passed through a dedicated API.
3.  **Generate:** A local desktop app pulls the JD and uses a **Local LLM** to synthesize a custom cover letter based on your unique profile.
4.  **Protect:** Your resume, history, and identity stay 100% offline.

## 🛠️ How we Built It
We combined modern AI capabilities with robust Software Engineering (SE) fundamentals:
* **Browser Plugin:** Custom extension for real-time JD scraping.
* **API & Backend:** Powered by **FastAPI** and hosted on **Render.com** to orchestrate data flow.
* **Local App:** A sleek, user-friendly interface built with **Streamlit**.
* **Brain:** **Ollama** running local LLMs (like Llama 3 or Mistral) for private, high-speed inference.

## 🚧 Challenges we Ran Into
The primary hurdle was optimizing **Local Compute** performance. Balancing the memory footprint of the LLM while maintaining the generation speed required for a seamless user experience taught us the nuances of efficient model deployment on consumer hardware.

## 🏆 Accomplishments that we're Proud Of
We successfully bridged the gap between modern AI and **classic SE**. We proved that high-utility AI doesn't require a cloud-first, data-harvesting model. We delivered a functional "Privacy-by-Design" framework that gives users a professional edge while maintaining 100% data sovereignty.

## 📚 What we Learned
While data is the fuel for modern AI, **good old SE tools** still form the backbone of the industry. We learned that the most impactful AI solutions are those that integrate seamlessly into existing workflows without compromising user security.

## 🔮 What's Next for LocalCraft.io-UMD
* **Resume Optimization:** Automated bullet-point tailoring for ATS compatibility.
* **Multi-Model Support:** One-click switching between different Ollama models.
* **Expanded Scraping:** Deep integration for LinkedIn, Indeed, and Greenhouse.

---

### **"Your data is yours. Your career is yours. Keep it that way."**

---
