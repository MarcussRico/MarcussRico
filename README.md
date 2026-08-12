<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,35:302b63,70:24243e,100:1a1a2e&height=260&section=header&text=Sai&fontSize=90&fontColor=ffffff&animation=twinkling&fontAlignY=32&desc=Agentic%20AI%20%E2%80%A2%20RAG%20%E2%80%A2%20LLMs%20%E2%80%A2%20Computer%20Vision&descAlignY=52&descSize=20&descColor=A970FF" width="100%" />

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=26&duration=2600&pause=700&color=A970FF&center=true&vCenter=true&width=800&height=90&lines=building+agents+that+actually+use+their+tools;RAG+pipelines+that+retrieve+the+right+thing;CSE+undergrad+%40+Chennai+Institute+of+Technology;honest+baselines+%3E+suspicious+accuracy+numbers" alt="Typing SVG" />

<br/>

<a href="mailto:saianandro@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" /></a>
<a href="https://github.com/MarcussRico"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" /></a>
<img src="https://komarev.com/ghpvc/?username=MarcussRico&style=for-the-badge&color=A970FF&label=PROFILE+VIEWS" />

<br/><br/>

<img src="https://img.shields.io/badge/Agentic%20AI-8A2BE2?style=for-the-badge&logo=robotframework&logoColor=white" />
<img src="https://img.shields.io/badge/RAG-6C3EF4?style=for-the-badge&logo=databricks&logoColor=white" />
<img src="https://img.shields.io/badge/LLMs-5865F2?style=for-the-badge&logo=openai&logoColor=white" />
<img src="https://img.shields.io/badge/Computer%20Vision-3D5AFE?style=for-the-badge&logo=opencv&logoColor=white" />

</div>

---

<img align="right" src="https://github-readme-stats-git-master-rickstaa.vercel.app/api?username=MarcussRico&show_icons=true&hide_border=true&title_color=A970FF&icon_color=A970FF&text_color=c9d1d9&bg_color=0d1117&include_all_commits=true&rank_icon=github" width="420" />

### `whoami`

```yaml
name:      Sai
role:      2nd-year CSE @ CIT Chennai
location:  Chennai, Tamil Nadu, India
focus:
  - agentic AI systems & multi-agent tool use
  - retrieval-augmented generation (RAG)
  - LLM application engineering
  - computer vision & remote sensing
building:  systems that reason, retrieve,
           and act — not just chat
```

I build applied ML systems end to end — from retrieval and tool orchestration for LLM agents, to vision models for real-world imagery. I care about the parts people skip: honest baselines, ablations that isolate one variable, and writing down what didn't work.

<br clear="right"/>

---

<div align="center">

## Tech Stack

<img src="https://skillicons.dev/icons?i=python,pytorch,tensorflow,sklearn,opencv,cpp,js,cs,fastapi,sqlite,git,linux,docker,unity,blender,vscode&perline=8" />

<br/><br/>

<img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" />
<img src="https://img.shields.io/badge/LlamaIndex-000000?style=flat-square&logo=llama&logoColor=white" />
<img src="https://img.shields.io/badge/Pinecone-000000?style=flat-square&logo=pinecone&logoColor=white" />
<img src="https://img.shields.io/badge/FAISS-00599C?style=flat-square&logo=meta&logoColor=white" />
<img src="https://img.shields.io/badge/OpenAI%20API-412991?style=flat-square&logo=openai&logoColor=white" />
<img src="https://img.shields.io/badge/Anthropic%20Claude-D97757?style=flat-square&logo=anthropic&logoColor=white" />
<img src="https://img.shields.io/badge/Groq-F55036?style=flat-square&logo=groq&logoColor=white" />
<img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black" />
<img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" />
<img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white" />
<img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" />
<img src="https://img.shields.io/badge/BeautifulSoup-59666C?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/CUDA-76B900?style=flat-square&logo=nvidia&logoColor=white" />
<img src="https://img.shields.io/badge/GDAL-5CAE58?style=flat-square&logo=qgis&logoColor=white" />
<img src="https://img.shields.io/badge/Sentinel--2-0B3D91?style=flat-square&logo=esa&logoColor=white" />

</div>

---

## Featured Work

<div align="center">
<a href="https://github.com/MarcussRico/deforestation-sentinel">
  <img src="https://github-readme-stats-git-master-rickstaa.vercel.app/api/pin/?username=MarcussRico&repo=deforestation-sentinel&hide_border=true&title_color=A970FF&icon_color=A970FF&text_color=c9d1d9&bg_color=0d1117" />
</a>
</div>

<br/>

<details open>
<summary><b>🤖 &nbsp;Data Analysis Harness — agent architecture for unseen datasets</b></summary>

<br/>

A harness that lets an LLM agent explore a dataset it has never seen, safely:

- **Sandboxed execution** — generated code runs isolated, not in the host process
- **Long-horizon memory** — findings persist across turns instead of falling out of context
- **Self-healing** — tool errors feed back as structured signal, the agent retries with a corrected call
- **Approval gates** — human in the loop before anything destructive runs

`Python` `tool-calling` `sandboxing` `agent-loops`

</details>

<details open>
<summary><b>🍜 &nbsp;Recipe Scraper — dataset pipeline for a food-focused LLM app</b></summary>

<br/>

Built a scraper to collect **~1,000,000 recipes** from sources like Yelp and Uber Eats Canada, cleaned and structured into a corpus feeding a food-focused LLM/RAG application — grounding generated recommendations in real menu and recipe data instead of the model's raw priors.

`Python` `BeautifulSoup` `web scraping` `data pipelines` `RAG corpus`

</details>

<details open>
<summary><b>🛰️ &nbsp;Deforestation Sentinel — satellite forest-loss detection</b></summary>

<br/>

| | |
|---|---|
| **Model** | ResNet50 transfer learning on EuroSAT |
| **Val accuracy** | `95.65%` |
| **Test accuracy** | `95.26%` |
| **Forest F1** | `0.9672` |
| **Real data** | Sentinel-2 L2A, AOI near Machadinho D'Oeste, Rondônia, Brazil |
| **Result** | 10 / 72 patches flagged Forest → non-forest (~410 ha estimated) |
| **Status** | Global Forest Watch alert cross-validation in progress |

A change-detection pipeline that goes from raw Sentinel-2 tiles to a ranked list of suspected clearing events. An earlier hackathon build wrapped the classifier in a multi-agent pipeline — **Baseline → Watcher → Triage → Escalation** — so alerts route themselves by severity instead of dumping into one queue.

`PyTorch` `ResNet50` `rasterio` `GDAL` `Sentinel-2` `OpenSwarm`

</details>

<details>
<summary><b>🧬 &nbsp;RNA-Binding Protein Binding Site Prediction <i>(one-off bioinformatics project)</i></b></summary>

<br/>

Predicting PUM2 binding sites directly from raw genomic sequence, trained on ENCODE eCLIP-seq data (`ENCSR661ICQ`, K562 cells).

| Architecture | ROC-AUC |
|---|---|
| Baseline CNN | `0.7473` |
| CNN + BiLSTM | `0.8206` |
| CNN + BiLSTM + Attention | `0.8197` |

The interesting result here is the null one — **attention matches BiLSTM accuracy while adding interpretable per-position weights at zero performance cost.** That makes interpretability free rather than a tradeoff.

`PyTorch` `pysam` `bedtools` `hg38` `eCLIP-seq`

</details>

<details>
<summary><b>🗂️ &nbsp;Earlier projects</b></summary>

<br/>

| Project | What it does | Stack |
|---|---|---|
| **Aide** | AI daily assistant — function-calling tools, whiteboard-photo → task extraction via vision, neural TTS | FastAPI, Groq, SQLite, vanilla JS |
| **Medical RAG Chatbot** | Retrieval-augmented QA over medical literature with grounded, cited answers | LLaMA 3.3, Groq, Pinecone, LangChain |
| **Gesture-Controlled Mouse** | Real-time cursor control from hand tracking on a standard webcam | MediaPipe, OpenCV |
| **Sign Language Detection** | CNN classifier for static sign recognition from video frames | TensorFlow, OpenCV |
| **Monocular Depth Estimation** | Dense depth maps from a single RGB image | MiDaS, PyTorch |
| **PDF Parser** | Structured extraction from unstructured PDFs, served over an API | pdfplumber, FastAPI |
| **Games** | Unity titles in C#, browser games in JS, 3D asset work | Unity, C#, JS, Blender |
| **MultipleLinearRegression** | Closed-form OLS written from scratch — reading the derivation and implementing it are not the same thing | NumPy |

</details>

---

<div align="center">

## Stats

<img src="https://github-readme-stats-git-master-rickstaa.vercel.app/api/streak/?user=MarcussRico&hide_border=true&background=0d1117&stroke=30363d&ring=A970FF&fire=A970FF&currStreakLabel=A970FF&sideLabels=c9d1d9&dates=8b949e&currStreakNum=c9d1d9&sideNums=c9d1d9" width="480" />
<img src="https://github-readme-stats-git-master-rickstaa.vercel.app/api/top-langs/?username=MarcussRico&layout=compact&hide_border=true&langs_count=8&title_color=A970FF&text_color=c9d1d9&bg_color=0d1117" width="340" />

<br/><br/>

<img src="https://github-trophies.vercel.app/?username=MarcussRico&theme=discord&no-frame=true&no-bg=true&row=1&column=7&margin-w=8" width="100%" />

<br/>

<img src="https://github-readme-activity-graph.vercel.app/graph?username=MarcussRico&bg_color=0d1117&color=c9d1d9&line=A970FF&point=ffffff&area=true&hide_border=true" width="100%" />

<br/>

<img src="https://raw.githubusercontent.com/MarcussRico/MarcussRico/output/snake.svg" alt="contribution snake" width="100%" />

</div>

---

<div align="center">

# How I Work

### *Solve the boring problem first. The interesting one is usually hiding behind it.*

</div>

<table>
<tr>
<td width="50%" valign="top">

**Baselines before optimization**
Get the dumbest version working end to end before tuning anything. A tuned pipeline built on a broken assumption is worse than a rough one built on a correct one.

**One variable at a time**
If two things changed between two results, the comparison is noise. Ablate, don't bundle.

**Write down what didn't work**
The failed run is data. Most of what looks like "trying random things" is actually just not keeping notes.

</td>
<td width="50%" valign="top">

**Honest numbers over impressive numbers**
I'd rather report a real `0.82` than a suspicious `0.97` I can't explain. If a result looks too good, the first suspect is the eval, not the model.

**Read the paper, then read the code**
The paper tells you what the method is supposed to do. The code tells you what it actually does. They disagree more often than people admit.

**Ship the thing that survives contact with real data**
Clean benchmarks are a starting point, not the goal. The real test is messy, incomplete, and doesn't look like the training set.

</td>
</tr>
</table>

---

<div align="center">

## Outside the terminal

<img src="https://img.shields.io/badge/Speedcubing-FF5800?style=for-the-badge&logo=rubikscube&logoColor=white" />
<img src="https://img.shields.io/badge/Swimming-0077B6?style=for-the-badge" />
<img src="https://img.shields.io/badge/-Chess-769656?style=flat-square&logo=lichess&logoColor=white" />

<br/><br/>

**Open to collaborating on agentic AI, RAG pipelines, and LLM-based systems** — also into applied ML for computer vision and remote sensing.

<a href="mailto:saianandro@gmail.com"><img src="https://img.shields.io/badge/saianandro@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white" /></a>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,30:24243e,65:302b63,100:0f0c29&height=140&section=footer" width="100%" />

</div>
