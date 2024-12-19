import yaml
import utils
from tqdm import tqdm
from collections import defaultdict

def main():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    with open(config['scene2plot']['story_input'], 'r', encoding='utf-8') as story_file:
        story_data = yaml.safe_load(story_file)
    
    with open(config['scene2plot']['scene_input'], 'r', encoding='utf-8') as scene_file:
        scene_data = yaml.safe_load(scene_file)
    
    plots = []
    
    story_scenes = defaultdict(list)
    for scene in scene_data['scenes']:
        story_scenes[scene['story_index']].append(scene)
    
    for story_index, scenes in tqdm(story_scenes.items(), desc='Processing Stories'):
        story = story_data['stories'][story_index]
        
        scenes.sort(key=lambda x: x['scene_index'])
        
        initial_prompt = (f"这是原始故事:\n{story}\n\n"
                        "接下来我会依次给你这个故事的5个场景，"
                        "请你为每个场景创作具体的剧情发展，"
                        "保持故事情节的连贯性和发展性。")
        
        chat_history = utils.init_chat(config['scene2plot']['SysPrompt'] + "\n" + initial_prompt)
        
        for scene in scenes:
            scene_prompt = (f"这是第{scene['scene_index']}个场景的描述:\n"
                          f"{scene['content']}\n"
                          "请基于前面的剧情发展，为这个场景创作具体的情节。")
            
            messages, response = utils.continue_chat(
                url=config['scene2plot']['url'],
                token=config['scene2plot']['token'],
                model=config['scene2plot']['model'],
                messages=chat_history,
                user_input=scene_prompt
            )
            
            chat_history = messages
            
            plot_content = {
                'story_index': story_index,
                'scene_index': scene['scene_index'],
                'plot': response['choices'][0]['message']['content']
            }
            plots.append(plot_content)
    
    output = config['scene2plot']['output']
    output_data = {'plots': plots}
    with open(output, 'w', encoding='utf-8') as file:
        yaml.dump(output_data, file, allow_unicode=True, sort_keys=False)
    
    print(f'Plots have been saved to {output}')

if __name__ == '__main__':
    main()