- 
      
      
        
      
      
      
- 
      
    
    
      
        GROBID Documentation
      
    
    
      
- 
      
        
        
- 
      
      

    
    
      
    
    
      
        
        
        
- 
        
- 
        
      
    
    
      
- 
    
    
    
      

    
    
  
  
  
    
    
      
    
    
    
    
    
  
    
    
    
    
    
      
        
        [Skip to content](#grobid-documentation)
      
    
    
      
    
    
    
      

  

  
      
    
    
      
        
          
            Initializing search
          
          
        
      
    
  

      
    
    
      
        [GitHub](https://github.com/grobidOrg/grobid/)
      
    
  
  

    
    
      
      
        
          
        
      
      
        
          
            
              
              
                
                  
                    

      
    
  

    
      
      
  
  
  
  
    
    
    
    
    
    
- 
      
        
        
        
        
          
          
            
  
  
  
    
  
    Getting Started
  

    
  
  
  

            
          
        
        
      
    
  

    
      
      
  
  
  
  
    
    
    
    
    
    
- 
      
        
        
        
        
          
          
            
  
  
  
    
  
    Upgrading
  

    
  
  
  

            
          
        
        
      
    
  

    
      
      
  
  
  
  
    
    
    
    
    
    
- 
      
        
        
        
        
          
          
            
  
  
  
    
  
    User Guide
  

    
  
  
  

            
          
        
        
      
    
  

    
      
      
  
  
  
  
    
    
    
    
    
    
- 
      
        
        
        
        
          
          
            
  
  
  
    
  
    About
  

    
  
  
  

            
          
        
        
      
    
  

    
      
      
  
  
  
  
    
    
    
    
    
    
- 
      
        
        
        
        
          
          
            
  
  
  
    
  
    Developer Guide
  

    
  
  
  

            
          
        
        
      
    
  

    
      
      
  
  
  
  
    
    
    
    
    
    
- 
      
        
        
        
        
          
          
            
  
  
  
    
  
    Annotation Guidelines
  

    
  
  
  

            
          
        
        
      
    
  

    
      
      
  
  
  
  
    
    
    
    
    
    
- 
      
        
        
        
        
          
          
            
  
  
  
    
  
    Benchmarking
  

    
  
  
  

            
          
        
        
      
    
  

    
      
      
  
  
  
  
    
    
    
    
    
    
- 
      
        
        
        
        
          
          
            
  
  
  
    
  
    Archive
  

    
  
  
  

            
          
        
        
      
    
  

    
  

                  
                
              
            
            
              
              
                
                  
                    

                  
                
              
            
          
          
            
              
              
                
                  

  
  

# GROBID Documentation

## Getting Started

New to GROBID? Start here to get up and running quickly.

- 

[Quick start](getting_started/) — install and launch GROBID in minutes

- 

[Run with Docker](Grobid-docker/) — the easiest way to deploy GROBID

- 

[Troubleshooting and FAQ](Frequently-asked-questions/) — common issues and solutions

## Upgrading

- [Upgrade guide](Upgrading/) — what to know when moving between major GROBID versions

## User Guide

Everything you need to use GROBID once it's running.

- 

[Using the REST API](Grobid-service/) — endpoints, parameters, and client libraries

- 

[Understanding the output (TEI)](TEI-encoding-of-results/) — structure of the TEI XML results

- 

[PDF coordinates](Coordinates-in-PDF/) — extracting bounding boxes for structures in the original PDF

- 

[Configuration](Configuration/) — tuning GROBID for your use case

- 

[Consolidation service](Consolidation/) — linking extracted references to external metadata

- 

[Specialized processes](Grobid-specialized-processes/) — patents, medical, and other domain-specific workflows

## About

- 

[Introduction](Introduction/) — what GROBID is and what it does

- 

[How GROBID works](Principles/) — architecture and processing pipeline

- 

[Benchmarks](benchmarks/Benchmarking/) — evaluation methodology and overview of results

- 

[References](References/) — publications about GROBID

- 

[License](License/)

- 

[Community](Community/) — mailing list, Discord, and how to get involved

## Developer Guide

Building, training, and extending GROBID.

- 

[Build from source](Install-Grobid/) — set up a development environment

- 

[Training and evaluating models](Training-the-models-of-Grobid/) — retrain or fine-tune GROBID models

- 

[End-to-end evaluation](End-to-end-evaluation/) — evaluate full pipeline performance

- 

[Deep Learning models](Deep-Learning-models/) — using DL models instead of default CRF

- 

[Developer notes](Notes-grobid-developers/) — internal conventions and tips for contributors

- 

[Recompiling CRF libraries](Recompiling-and-integrating-CRF-libraries/) — rebuilding native CRF dependencies

## Annotation Guidelines

Guidelines for annotating training data.

- 

[General principles](training/General-principles/)

- 

[Segmentation model](training/segmentation/)

- 

[Fulltext model](training/fulltext/)

- 

[Header model](training/header/)

- 

[Bibliographical references](training/Bibliographical-references/)

- 

[Affiliation-address model](training/affiliation-address/)

- 

[Date model](training/date/)

## Benchmarking

Detailed evaluation results on specific datasets.

- 

[PubMed Central](benchmarks/Benchmarking-pmc/)

- 

[bioRxiv](benchmarks/Benchmarking-biorxiv/)

- 

[PLOS](benchmarks/Benchmarking-plos/)

- 

[eLife](benchmarks/Benchmarking-elife/)

- 

[Model comparison](benchmarks/Benchmarking-models/)

## Archive

Deprecated features kept for reference.

- 

[Batch mode (deprecated)](Grobid-batch/)

- 

[Java library (deprecated)](Grobid-java-library/)

                
              
            
          
          

        
        
      
      
        
  
  
    
      
  
  
    Made with
    [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)