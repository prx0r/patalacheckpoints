- 
  
- 
  
- 
  
- 
  
- 
  
- 

  

  
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 

  

    
- 
    
- 
    
- 
    
- 
  
- 

- 

  

  

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

  
  
- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

  
- 

- 

- 

  GitHub - yale-nlp/SciRAG · GitHub

  
  
  
  

    
  

  

    

  
  

  
  
- 

    

  

  

    

  

    

    

      

      
- 

    
- 
    
    

      
  
  

      

        

  
  
  
  

  

      

    

  

  
  

    

    
  

  

  

    
  

  
- 
  
- 
  
- 

  
- 

  

  
    
      
      

    
      [Skip to content](#start-of-content)

      
    
      
      
- 

- 

- 

- 

  
  
  

      

          

                
- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

- 

  
  
  ## Navigation Menu
[](/)[Sign in](/login?return_to=https%3A%2F%2Fgithub.com%2Fyale-nlp%2FSciRAG)

Appearance settings

Type / to search[Sign in](/login?return_to=https%3A%2F%2Fgithub.com%2Fyale-nlp%2FSciRAG)[Sign up](/signup?ref_cta=Sign+up&amp;ref_loc=header+logged+out&amp;ref_page=%2F%3Cuser-name%3E%2F%3Crepo-name%3E&amp;source=header-repo&amp;source_repo=yale-nlp%2FSciRAG)

Appearance settings

      
  
        
    

        You signed in with another tab or window. Reload to refresh your session.
        You signed out in another tab or window. Reload to refresh your session.
        You switched accounts on another tab or window. Reload to refresh your session.

      
    

Dismiss alert

  

    

  

    

  
    

  
    
      
    

    
    
      
      {{ message }}

    
  

  

    

  
        
    
      
      
    

    
  
  
    
  
    
      

      ### Uh oh!

      

        

There was an error while loading. Please reload this page.

  
  

    

  

  

      

        
            
  
      
    

    
    
      [yale-nlp](/yale-nlp)    
    /
    
      [SciRAG](/yale-nlp/SciRAG)
    

    Public
  

        

        
            
    
      

  
- 
            [Notifications](/login?return_to=%2Fyale-nlp%2FSciRAG)    You must be signed in to change notification settings

  

  
- 
          [Fork
    0](/login?return_to=%2Fyale-nlp%2FSciRAG)
  

  
- 
        
        [Star
          14](/login?return_to=%2Fyale-nlp%2FSciRAG)
  

        
      

        

          

  
  

    
    

    
      
    

  
  
    [](/yale-nlp/SciRAG) 

main

[Branches](/yale-nlp/SciRAG/branches)[Tags](/yale-nlp/SciRAG/tags)[](/yale-nlp/SciRAG/branches)[](/yale-nlp/SciRAG/tags)Go to file

Code

Open more actions menu## Folders and files
NameNameLast commit messageLast commit date## Latest commit
 ## History
[7 Commits](/yale-nlp/SciRAG/commits/main/)[](/yale-nlp/SciRAG/commits/main/)7 Commits

[assets](/yale-nlp/SciRAG/tree/main/assets)

[assets](/yale-nlp/SciRAG/tree/main/assets)  

[longans](/yale-nlp/SciRAG/tree/main/longans)

[longans](/yale-nlp/SciRAG/tree/main/longans)  

[shortans](/yale-nlp/SciRAG/tree/main/shortans)

[shortans](/yale-nlp/SciRAG/tree/main/shortans)  

[README.md](/yale-nlp/SciRAG/blob/main/README.md)

[README.md](/yale-nlp/SciRAG/blob/main/README.md)  

[environment.yml](/yale-nlp/SciRAG/blob/main/environment.yml)

[environment.yml](/yale-nlp/SciRAG/blob/main/environment.yml)  View all files## Repository files navigation

# SciRAG: Adaptive, Citation-Aware, and Outline-Guided Retrieval and Synthesis for Scientific Literature
[](#scirag-adaptive-citation-aware-and-outline-guided-retrieval-and-synthesis-for-scientific-literature)

[](https://arxiv.org/pdf/2511.14362)

## 📖 Overview
[](#-overview)

  [](/yale-nlp/SciRAG/blob/main/assets/overview.png)

Existing baseline approaches for scientific question answering follow a single-threaded iterative retrieval strategy, limiting their ability to comprehensively address multi-faceted questions and leading to incomplete coverage and answer organization.

SciRAG addresses these limitations through a novel framework with three key capabilities:

- Adaptive Retrieval: A Gap Critic mechanism automatically determines when additional retrieval is needed and uses tree-based query decomposition to enable parallel or sequential exploration of sub-questions, with citation graph expansion to enrich the retrieved paper set.

- Symbolic Reasoning-Based Reranking: A three-step symbolic reasoning process analyzes paper relationships and contributions to intelligently rerank retrieved documents.

- Outline-Guided Synthesis: Answers are synthesized through bottom-up aggregation along the query tree, guided by a structured outline to ensure comprehensive coverage and proper organization.

SciRAG achieves strong performance across both long-form literature review tasks (ScholarQA, QASA) and short-form answer tasks (SciFact, PubMedQA), demonstrating superior answer quality compared to existing baselines.
## 🏗️ Framework
[](#️-framework)

  [](/yale-nlp/SciRAG/blob/main/assets/framework.png)

## 🚀 Quickstart
[](#-quickstart)
### 📦 Installation
[](#-installation)

Create and activate the conda environment:

conda env create -f environment.yml
conda activate scirag

Remember to configure your API keys:

- Set your Semantic Scholar API key in `web_search.py`

- Set your LLM API key in `config.yaml`

### ▶️ Running the Pipeline
[](#️-running-the-pipeline)

For long-form answers (ScholarQA, QASA):

cd longans
python run.py --input_file test.jsonl --output_file testout.jsonl --model_name gpt4o

For short-form answers (SciFact, PubMedQA):

cd shortans/scifact  # or shortans/pubmed
python run.py --input_file test.jsonl --output_file testout.jsonl --model_name gpt4o
### 🔍 Initial Dense Retrieval
[](#-initial-dense-retrieval)

Since dense retrieval from a large-scale corpus (45 million papers) can be resource-intensive, we recommend following the retrieval method from:

[OpenScholar Retriever](https://github.com/AkariAsai/OpenScholar/tree/main/retriever)

This helps reduce the heavy resource cost during retrieval. Once retrieved, you can use the output file as the input to the SciRAG pipeline.
### 📊 Evaluation
[](#-evaluation)

For evaluation tools and benchmarks, please refer to:

[ScholarQABench](https://github.com/AkariAsai/ScholarQABench/tree/main)
## ✍️ Citation
[](#️-citation)

If you use our work and are inspired by our work, please consider cite us:

```
@misc{ding2025sciragadaptivecitationawareoutlineguided,
      title={SciRAG: Adaptive, Citation-Aware, and Outline-Guided Retrieval and Synthesis for Scientific Literature}, 
      author={Hang Ding and Yilun Zhao and Tiansheng Hu and Manasi Patwardhan and Arman Cohan},
      year={2025},
      eprint={2511.14362},
      archivePrefix={arXiv},
      primaryClass={cs.DL},
      url={https://arxiv.org/abs/2511.14362}, 
}
```

## About
No description, website, or topics provided.### Resources
[Readme](#readme-ov-file)[Activity](/yale-nlp/SciRAG/activity)[Custom properties](/yale-nlp/SciRAG/custom-properties)### Stars

14 stars### Watchers

2 watching### Forks
[0 forks](/yale-nlp/SciRAG/forks)[Report repository](/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fyale-nlp%2FSciRAG&amp;report=yale-nlp+%28user%29)## Releases
## Packages
## Contributors
## Languages
   

  

    
  

  

          
  ## Footer

  

  
    
      [](https://github.com)
      
        &copy; 2026 GitHub,&nbsp;Inc.
      
    

    
  

    

  
    
    

    
      
    

    
    You can’t perform that action at this time.