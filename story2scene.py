import yaml
import utils
import pandas as pd
from tqdm import tqdm

def main():
    with open('config.yaml','r') as file:
        config = yaml.safe_load(file)
        
    with open(config['story2scene']['input'],'r',encoding='utf-8') as file:
        storys_file = yaml.safe_load(file)
        scenes = []
        print(config['sentence2story']['SysPrompt'])
        for story in tqdm(storys_file['storys'],desc='Storys Loop',leave=False):
            response = utils.chat(
                url=config['story2scene']['url'],
                token=config['story2scene']['token'],
                model=config['story2scene']['model'],
                system_prompt=config['story2scene']['SysPrompt'],
                query=story
            )
            scenes.append(response['choices'][0]['message']['content'])
        output = config['story2scene']['output']
        output_data = {'scenes':scenes}
        with open(output,'w',encoding='utf-8') as file:
            yaml.dump(output_data,file,allow_unicode=True)
    print(f'Scenes have been saved to {output}')

if __name__ == '__main__':
  main()