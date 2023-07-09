
<p align="center">
  <img width="180" src="./images/logo.png" alt="GPTerm">
  <h1 align="center">GPTerm</h1>
</p>


This project focuses on converting plain text into shell commands using different models, including ChatGPT and various open-source language models. While some models yielded good results, others did not meet the desired level of success. The project primarily utilized iTerm as the terminal application for testing, but assessments with other terminals have yet to be conducted as the emphasis is on running and comparing the models. However, it is anticipated that other terminal applications would also be suitable for this project.

The project consists of two main parts. In the first part, users can manually enter and execute shell commands without closing the plugin. The second part involves translating given plain text into shell commands, which are then presented to the user. Users have the flexibility to modify or delete sections of the generated command without execution, if desired. Both sections operate in a similar manner. To indicate the intention of obtaining shell commands from plain text only, users need to prefix the plain text with dot (.). This allows the application to distinguish between manual command entry and obtaining commands from plain text.


This project tests four models for performance and results. ChatGPT initially shows the best outcomes due to its cost-effective low token count for generating shell commands. Alpaca with 7 billion parameters doesn't perform well, while the MPT model performs better but has occasional incorrect responses. WizardCoder outperforms both Alpaca and MPT, offering acceptable results for open-source model users. However, it is still behind ChatGPT.

It is worth mentioning that while ChatGPT delivers results in a well-organized JSON structure, other open-source models may sometimes provide noisy responses to inquiries. To handle such situations, the [json_extractor](/src/responser.py) function is utilized to eliminate any noise present in the responses of other open-source models..
This part can be developed further.

All packages are installed before starting.  The following command is used for this installation process (python 3.8 is used in this project):


## Usage

To begin with, **it is recommended to work within an environment.** In this project, the conda environment "py1" (sample conda env name) is utilized for development. Then;

```
  pip3 install gpterm-tool
```
You can run the provided above command for installation purposes.  Once installed, it can be utilized by using the 'gpterm' keyword on iTerm or any other terminal application.
- Run with ChatGPT model (Highly Recommended)
```
  gpterm -k <openai_api_key>
```
- Run with mpt model
```
gpterm -m mpt -p <quantized_mpt_model_path>
```
- Run with wizardcoder model
```
gpterm -m wizardcoder -p <quantized_wizardcoder_model_path>
```

As the models used have a large number of parameters and are executed on the CPU, the processing speed of the results may be slower. The project was developed on an M1 MacBook Pro, and no tests with GPU implementation have been performed yet. Hence, for professional use, it is recommended to opt for the ChatGPT model.
  
For swift access and usage of this program, you have the option to include an alias in the zshrc file. This allows for convenient and rapid execution of the program. My conda env name is py1. 
```
 alias gt='conda activate py1 && gpterm -k <openai_api_key>'
```
Following that, the program can be easily launched via the terminal by simply entering the "gp" keyword.  

If you are interested in running the models using GPU acceleration, you can refer to the link provided below for further information and instructions.
https://github.com/marella/ctransformers  


## ChatGPT vs WizardCoder
- ChatGPT   
```
name_ai ---> . go in storage folder and sort only pdf files reversely

>>> cd storage && ls -r *.pdf

name_ai ---> . Create a folder named sample_1 and create a txt file for each number starting from 1 to 10 in it and assign that number as the name

>>> mkdir sample_1 && for i in {1..10}; do touch sample_1/$i.txt; done

name_ai ---> . Create a file named nw_1 with .txt extension and add all the numbers from 1 to 10 in it

>>> touch nw_1.txt; echo {1..10} >> nw_1.txt
```
- WizardCoder
```
name_ai ---> . go in storage folder and sort only pdf files reversely

>>> ls -l storage | grep pdf | sort -r

name_ai ---> . Create a folder named sample_1 and create a txt file for each number starting from 1 to 10 in it and assign that number as the name

>>> mkdir sample_1 && cd sample_1 \\ Wrong one here !

name_ai ---> . Create a file named nw_1 with .txt extension and add all the numbers from 1 to 10 in it

>>> touch nw_1.txt && echo '1 2 3 4 5 6 7 8 9 10' >> nw_1.txt
```

As observed earlier, ChatGPT provides highly accurate responses. In the WizardCoder model, it successfully generated the correct command in two out of the three requests, although it did produce an incorrect command in one request. Sometimes MPT and WizardCoder models return our prompt as result. **Remember! The ChatGPT model is highly suitable for implementation, while the others are still in the experimental phase. They are not suitable for use yet.**

_**Note:** As previously explained, it is important to note that open-source models may sometimes produce noisy results. To solve this issue, the [json_extractor](/src/responser.py) function is utilized to filter out any unwanted noise and obtain the desired outcome. This function can be adjusted to handle JSONDecodeError exceptions, ensuring smooth execution. In future iterations, the regex pattern will be refined to encompass all possible error cases. However, for the current implementation, the pattern has been tailored to address the most prevalent sources of noise, considering the constraints of time. However, in the current implementation, the pattern has been adjusted to effectively handle the main sources of noise, taking into account the time limitations._


## TODOS

- [X] Test of ChatGPT
- [X] Test of WizardCoder
- [X] Test of MPT
- [ ] Test of Alpaca
- [ ] Test of StarCoder
- [ ] Upgrade [json_extractor](/src/responser.py) (regex pattern)
- [ ] Running models on GPU
- [ ] Train opensource models
