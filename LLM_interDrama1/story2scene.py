import yaml
import utils
import pandas as pd
from tqdm import tqdm

def main():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        
    with open(config['story2scene']['input'], 'r', encoding='utf-8') as file:
        stories_file = yaml.safe_load(file)
        scenes = []
        
        for story in tqdm(stories_file['stories'], desc='stories Loop', leave=False):
            chat_history = utils.init_chat(config['story2scene']['SysPrompt'] + "\n这是提供的故事:\n" + story)
            
            for i in range(1, 6):
                messages, response = utils.continue_chat(
                    url=config['story2scene']['url'],
                    token=config['story2scene']['token'],
                    model=config['story2scene']['model'],
                    messages=chat_history,
                    user_input=f"现在请你生成相应的场景{i}"
                )
                
                chat_history = messages
                
                scene_content = {
                    'story_index': stories_file['stories'].index(story),
                    'scene_index': i,
                    'content': response['choices'][0]['message']['content']
                }
                scenes.append(scene_content)
        
        output = config['story2scene']['output']
        output_data = {'scenes': scenes}
        with open(output, 'w', encoding='utf-8') as file:
            yaml.dump(output_data, file, allow_unicode=True, sort_keys=False)
            
    print(f'Scenes have been saved to {output}')

if __name__ == '__main__':
    main()