<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:203a43,100:2c5364&height=200&section=header&text=Sai&fontSize=80&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Applied%20ML%20%E2%80%A2%20Computer%20Vision%20%E2%80%A2%20Computational%20Biology%20%E2%80%A2%20Agents&descAlignY=55&descSize=18" width="100%" />

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=800&color=58A6FF&center=true&vCenter=true&width=650&lines=CSE+undergrad+%40+Chennai+Institute+of+Technology;I+train+models+on+satellites%2C+genomes%2C+and+agents;400%2B+LeetCode+problems+solved;Honest+baselines+%3E+suspicious+accuracy+numbers" alt="Typing SVG" />

<br/>

<a href="mailto:saianandro@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" /></a>
<a href="https://github.com/MarcussRico"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" /></a>
<a href="https://lichess.org/"><img src="https://img.shields.io/badge/Lichess-000000?style=for-the-badge&logo=lichess&logoColor=white" /></a>
<img src="https://komarev.com/ghpvc/?username=MarcussRico&style=for-the-badge&color=58A6FF&label=PROFILE+VIEWS" />

</div>

---

<img align="right" src="https://github-readme-stats.vercel.app/api?username=MarcussRico&show_icons=true&hide_border=true&title_color=58A6FF&icon_color=58A6FF&text_color=c9d1d9&bg_color=0d1117&include_all_commits=true&rank_icon=github" width="420" />

### `whoami`

```yaml
name:      Sai
role:      2nd-year CSE @ CIT Chennai
location:  Chennai, Tamil Nadu, India
focus:
  - computer vision & remote sensing
  - deep learning for genomics
  - agentic AI systems & tool use
building:  models that survive contact
           with real, messy data
gpu:       RTX 4070 Ti Super
stack:     VS Code + Obsidian + Notion
```

I build machine learning systems end to end — data acquisition, model design, training, evaluation, and the deployment layer around them. I care about the parts people skip: honest baselines, ablations that isolate one variable, and writing down what didn't work.

<br clear="right"/>

---

<div align="center">

## Tech Stack

<img src="https://skillicons.dev/icons?i=python,pytorch,tensorflow,sklearn,opencv,cpp,js,cs,fastapi,sqlite,git,linux,docker,unity,blender,vscode&perline=8" />

<br/><br/>

<img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" />
<img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white" />
<img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" />
<img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black" />
<img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" />
<img src="https://img.shields.io/badge/Pinecone-000000?style=flat-square&logo=pinecone&logoColor=white" />
<img src="https://img.shields.io/badge/Groq-F55036?style=flat-square&logo=groq&logoColor=white" />
<img src="https://img.shields.io/badge/CUDA-76B900?style=flat-square&logo=nvidia&logoColor=white" />
<img src="https://img.shields.io/badge/GDAL-5CAE58?style=flat-square&logo=qgis&logoColor=white" />
<img src="https://img.shields.io/badge/Sentinel--2-0B3D91?style=flat-square&logo=esa&logoColor=white" />

</div>

---

## Featured Work

<div align="center">
<a href="https://github.com/MarcussRico/deforestation-sentinel">
  <img src="https://github-readme-stats.vercel.app/api/pin/?username=MarcussRico&repo=deforestation-sentinel&hide_border=true&title_color=58A6FF&icon_color=58A6FF&text_color=c9d1d9&bg_color=0d1117" />
</a>
</div>

<br/>

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
<summary><b>🧬 &nbsp;RNA-Binding Protein Binding Site Prediction</b></summary>

<br/>

Predicting PUM2 binding sites directly from raw genomic sequence, trained on ENCODE eCLIP-seq data (`ENCSR661ICQ`, K562 cells).

| Architecture | ROC-AUC |
|---|---|
| Baseline CNN | `0.7473` |
| CNN + BiLSTM | `0.8206` |
| CNN + BiLSTM + Attention | `0.8197` |

The interesting result here is the null one — **attention matches BiLSTM accuracy while adding interpretable per-position weights at zero performance cost.** That makes interpretability free rather than a tradeoff. Next step is validating those attention peaks against known PUM2 motifs with a collaborator on the genomics side.

`PyTorch` `pysam` `bedtools` `hg38` `eCLIP-seq`

</details>

<details>
<summary><b>🤖 &nbsp;Data Analysis Harness — agent architecture for unseen datasets</b></summary>

<br/>

A harness that lets an LLM agent explore a dataset it has never seen, safely:

- **Sandboxed execution** — generated code runs isolated, not in the host process
- **Long-horizon memory** — findings persist across turns instead of falling out of context
- **Self-healing** — tool errors feed back as structured signal, the agent retries with a corrected call
- **Approval gates** — human in the loop before anything destructive runs

`Python` `tool-calling` `sandboxing` `agent-loops`

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

<img src="https://streak-stats.demolab.com?user=MarcussRico&hide_border=true&background=0d1117&stroke=30363d&ring=58A6FF&fire=58A6FF&currStreakLabel=58A6FF&sideLabels=c9d1d9&dates=8b949e&currStreakNum=c9d1d9&sideNums=c9d1d9" width="480" />
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=MarcussRico&layout=compact&hide_border=true&langs_count=8&title_color=58A6FF&text_color=c9d1d9&bg_color=0d1117" width="340" />

<br/><br/>

<img src="https://github-profile-trophy.vercel.app/?username=MarcussRico&theme=discord&no-frame=true&no-bg=true&row=1&column=7&margin-w=8" width="100%" />

<br/>

<img src="https://github-readme-activity-graph.vercel.app/graph?username=MarcussRico&bg_color=0d1117&color=c9d1d9&line=58A6FF&point=ffffff&area=true&hide_border=true" width="100%" />

<br/>

<img src="https://raw.githubusercontent.com/MarcussRico/MarcussRico/output/snake.svg" alt="contribution snake" width="100%" />

</div>

---

<div align="center">

## Competitive Programming

<img src="https://leetcard.jacoblin.cool/X7_Sai?theme=dark&font=Fira%20Code&ext=heatmap" width="620" />

</div>

**400+ problems solved.** Contest practice is what I lean on hardest when I hit an unfamiliar research problem — a lot of "novel" problems turn out to be a known technique wearing a different hat. Finalist at the SRM Vadapalani state-level codathon.

---

## How I work

```
├── Notion      → ML knowledge base. Solved once, written down forever.
├── Obsidian    → PARA-structured second brain, synced to Drive
├── Training    → RTX 4070 Ti Super for heavy runs, MacBook Air for everything else
├── References  → text over video — Raschka, ISLR, nanoGPT, papers
└── Principle   → I'd rather report an honest 0.82 AUC than a suspicious 0.97
```

---

<div align="center">

## Outside the terminal

<img src="https://img.shields.io/badge/Speedcubing-FF5800?style=for-the-badge&logo=rubikscube&logoColor=white" />
<img src="https://img.shields.io/badge/Swimming-0077B6?style=for-the-badge" />
<img src="https://img.shields.io/badge/Chess-769656?style=for-the-badge&logo=lichess&logoColor=white" />

<br/><br/>

**Open to collaborating on applied ML research** — remote sensing, computational biology, or agent systems.

<a href="mailto:saianandro@gmail.com"><img src="https://img.shields.io/badge/saianandro@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white" /></a>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2c5364,50:203a43,100:0f2027&height=120&section=footer" width="100%" />

</div>
