import yaml
import utils
import pandas as pd
from tqdm import tqdm

def main():
    with open('config.yaml','r') as file:
        config = yaml.safe_load(file)
    print(config['scene2detailed']['SysPrompt'])
    story_file = open(config['scene2detailed']['story_input'])
    scene_file = open(config['scene2detailed']['scene_input'])    
    storys = yaml.safe_load(story_file)
    scenes = yaml.safe_load(scene_file)
    combined_inputs = zip(storys['storys'], scenes['scenes'])
    details = []
    for story,scene in tqdm(combined_inputs,desc='Story and Scene Loop',leave=False):
        combined_input = f'{story}\n{scene}'
        response = utils.chat(
            url=config['scene2detailed']['url'],
            token=config['scene2detailed']['token'],
            model=config['scene2detailed']['model'],
            system_prompt=config['scene2detailed']['SysPrompt'],
            query=combined_input
        )
        details.append(response['choices'][0]['message']['content'])
    output = config['scene2detailed']['output']
    output_data = {'details':details}
    with open(output,'w',encoding='utf-8') as file:
        yaml.dump(output_data,file,allow_unicode=True)
    print(f'Scenes have been saved to {output}')

if __name__ == '__main__':
  main()