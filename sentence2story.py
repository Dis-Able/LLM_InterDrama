import yaml
import utils
import pandas as pd
from tqdm import tqdm

def main():
    with open('config.yaml','r') as file:
        config = yaml.safe_load(file)
        
    with open(config['sentence2story']['input'],'r',encoding='utf-8') as file:
        sentences_file = yaml.safe_load(file)
        storys = []
        print(config['sentence2story']['SysPrompt'])
        for sentence in tqdm(sentences_file['sentences'],desc='Sentence Loop',leave=False):
            print(sentence)
            response = utils.chat(
                url=config['sentence2story']['url'],
                token=config['sentence2story']['token'],
                model=config['sentence2story']['model'],
                system_prompt=config['sentence2story']['SysPrompt'],
                query=sentence
            )
            storys.append(response['choices'][0]['message']['content'])
        output = config['sentence2story']['output']
        output_data = {'storys':storys}
        with open(output,'w',encoding='utf-8') as file:
            yaml.dump(output_data,file,allow_unicode=True)
    print(f'Storys have been saved to {output}')

if __name__ == '__main__':
  main()