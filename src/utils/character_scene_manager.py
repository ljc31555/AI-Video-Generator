import os
import json
from typing import Dict, List, Any, Optional
from utils.logger import logger

class CharacterSceneManager:
    """角色场景数据库管理器 - 负责管理项目中的角色和场景一致性数据"""
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.database_dir = os.path.join(project_root, 'character_scene_db')
        os.makedirs(self.database_dir, exist_ok=True)
        
        # 数据库文件路径
        self.characters_file = os.path.join(self.database_dir, 'characters.json')
        self.scenes_file = os.path.join(self.database_dir, 'scenes.json')
        self.consistency_rules_file = os.path.join(self.database_dir, 'consistency_rules.json')
        
        # 初始化数据结构
        self._init_database_files()
    
    def _init_database_files(self):
        """初始化数据库文件"""
        # 初始化角色数据库
        if not os.path.exists(self.characters_file):
            default_characters = {
                "characters": {},
                "last_updated": "",
                "version": "1.0"
            }
            self._save_json(self.characters_file, default_characters)
        
        # 初始化场景数据库
        if not os.path.exists(self.scenes_file):
            default_scenes = {
                "scenes": {},
                "scene_categories": {
                    "indoor": ["家庭", "办公室", "教室", "餐厅", "卧室", "客厅", "厨房", "浴室"],
                    "outdoor": ["街道", "公园", "广场", "山林", "海边", "田野", "城市", "乡村"],
                    "special": ["梦境", "回忆", "幻想", "虚拟空间"]
                },
                "last_updated": "",
                "version": "1.0"
            }
            self._save_json(self.scenes_file, default_scenes)
        
        # 初始化一致性规则
        if not os.path.exists(self.consistency_rules_file):
            default_rules = {
                "character_consistency": {
                    "appearance_keywords": ["外貌", "长相", "身材", "发型", "眼睛", "肤色"],
                    "clothing_keywords": ["服装", "衣服", "穿着", "打扮", "装扮"],
                    "personality_keywords": ["性格", "气质", "表情", "神态", "情绪"]
                },
                "scene_consistency": {
                    "environment_keywords": ["环境", "背景", "场所", "地点", "位置"],
                    "lighting_keywords": ["光线", "照明", "明暗", "阴影", "光影"],
                    "atmosphere_keywords": ["氛围", "气氛", "情调", "感觉", "风格"]
                },
                "last_updated": "",
                "version": "1.0"
            }
            self._save_json(self.consistency_rules_file, default_rules)
    
    def _save_json(self, file_path: str, data: Dict):
        """保存JSON数据到文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存JSON文件失败 {file_path}: {e}")
    
    def _load_json(self, file_path: str) -> Dict:
        """从文件加载JSON数据"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"加载JSON文件失败 {file_path}: {e}")
        return {}
    
    def extract_characters_from_text(self, text: str) -> List[Dict[str, Any]]:
        """从文本中提取角色信息
        
        Args:
            text: 输入文本
            
        Returns:
            List[Dict]: 提取的角色信息列表
        """
        characters = []
        
        # 简单的角色提取逻辑（可以后续集成更复杂的NLP模型）
        character_indicators = [
            "主角", "主人公", "男主", "女主", "主要人物",
            "老师", "学生", "医生", "护士", "警察", "司机",
            "父亲", "母亲", "儿子", "女儿", "朋友", "同事"
        ]
        
        # 查找角色关键词
        found_characters = set()
        for indicator in character_indicators:
            if indicator in text:
                found_characters.add(indicator)
        
        # 为每个找到的角色创建基础信息
        for char_name in found_characters:
            character_info = {
                "name": char_name,
                "description": "",
                "appearance": {
                    "gender": "",
                    "age_range": "",
                    "height": "",
                    "hair": "",
                    "eyes": "",
                    "skin": "",
                    "build": ""
                },
                "clothing": {
                    "style": "",
                    "colors": [],
                    "accessories": []
                },
                "personality": {
                    "traits": [],
                    "expressions": [],
                    "mannerisms": []
                },
                "consistency_prompt": "",
                "extracted_from_text": True,
                "manual_edited": False
            }
            characters.append(character_info)
        
        return characters
    
    def extract_scenes_from_text(self, text: str) -> List[Dict[str, Any]]:
        """从文本中提取场景信息
        
        Args:
            text: 输入文本
            
        Returns:
            List[Dict]: 提取的场景信息列表
        """
        scenes = []
        
        # 场景关键词
        scene_keywords = {
            "indoor": ["房间", "屋内", "室内", "家里", "办公室", "教室", "餐厅", "卧室", "客厅", "厨房", "浴室", "商店", "医院", "银行"],
            "outdoor": ["街道", "马路", "公园", "广场", "山上", "海边", "田野", "森林", "花园", "院子", "阳台", "天台"],
            "time": ["早晨", "上午", "中午", "下午", "傍晚", "晚上", "深夜", "黎明", "黄昏"],
            "weather": ["晴天", "阴天", "雨天", "雪天", "多云", "雾天"]
        }
        
        found_scenes = set()
        scene_details = {}
        
        # 提取场景信息
        for category, keywords in scene_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    found_scenes.add(keyword)
                    if keyword not in scene_details:
                        scene_details[keyword] = {
                            "category": category,
                            "keyword": keyword
                        }
        
        # 为每个找到的场景创建详细信息
        for scene_name in found_scenes:
            scene_info = {
                "name": scene_name,
                "category": scene_details[scene_name]["category"],
                "description": "",
                "environment": {
                    "location_type": scene_details[scene_name]["category"],
                    "size": "",
                    "layout": "",
                    "decorations": [],
                    "furniture": []
                },
                "lighting": {
                    "time_of_day": "",
                    "light_source": "",
                    "brightness": "",
                    "mood": ""
                },
                "atmosphere": {
                    "style": "",
                    "colors": [],
                    "mood": "",
                    "weather": ""
                },
                "consistency_prompt": "",
                "extracted_from_text": True,
                "manual_edited": False
            }
            scenes.append(scene_info)
        
        return scenes
    
    def save_character(self, character_id: str, character_data: Dict[str, Any]):
        """保存角色信息
        
        Args:
            character_id: 角色ID
            character_data: 角色数据
        """
        try:
            characters_db = self._load_json(self.characters_file)
            characters_db["characters"][character_id] = character_data
            characters_db["last_updated"] = self._get_current_time()
            self._save_json(self.characters_file, characters_db)
            logger.info(f"角色信息已保存: {character_id}")
        except Exception as e:
            logger.error(f"保存角色信息失败: {e}")
    
    def save_scene(self, scene_id: str, scene_data: Dict[str, Any]):
        """保存场景信息
        
        Args:
            scene_id: 场景ID
            scene_data: 场景数据
        """
        try:
            scenes_db = self._load_json(self.scenes_file)
            scenes_db["scenes"][scene_id] = scene_data
            scenes_db["last_updated"] = self._get_current_time()
            self._save_json(self.scenes_file, scenes_db)
            logger.info(f"场景信息已保存: {scene_id}")
        except Exception as e:
            logger.error(f"保存场景信息失败: {e}")
    
    def get_character(self, character_id: str) -> Optional[Dict[str, Any]]:
        """获取角色信息
        
        Args:
            character_id: 角色ID
            
        Returns:
            Optional[Dict]: 角色数据
        """
        characters_db = self._load_json(self.characters_file)
        return characters_db.get("characters", {}).get(character_id)
    
    def get_scene(self, scene_id: str) -> Optional[Dict[str, Any]]:
        """获取场景信息
        
        Args:
            scene_id: 场景ID
            
        Returns:
            Optional[Dict]: 场景数据
        """
        scenes_db = self._load_json(self.scenes_file)
        return scenes_db.get("scenes", {}).get(scene_id)
    
    def get_all_characters(self) -> Dict[str, Any]:
        """获取所有角色信息"""
        characters_db = self._load_json(self.characters_file)
        return characters_db.get("characters", {})
    
    def get_all_scenes(self) -> Dict[str, Any]:
        """获取所有场景信息"""
        scenes_db = self._load_json(self.scenes_file)
        return scenes_db.get("scenes", {})
    
    def delete_character(self, character_id: str):
        """删除角色信息"""
        try:
            characters_db = self._load_json(self.characters_file)
            if character_id in characters_db.get("characters", {}):
                del characters_db["characters"][character_id]
                characters_db["last_updated"] = self._get_current_time()
                self._save_json(self.characters_file, characters_db)
                logger.info(f"角色信息已删除: {character_id}")
        except Exception as e:
            logger.error(f"删除角色信息失败: {e}")
    
    def delete_scene(self, scene_id: str):
        """删除场景信息"""
        try:
            scenes_db = self._load_json(self.scenes_file)
            if scene_id in scenes_db.get("scenes", {}):
                del scenes_db["scenes"][scene_id]
                scenes_db["last_updated"] = self._get_current_time()
                self._save_json(self.scenes_file, scenes_db)
                logger.info(f"场景信息已删除: {scene_id}")
        except Exception as e:
            logger.error(f"删除场景信息失败: {e}")
    
    def generate_consistency_prompt(self, character_ids: List[str] = None, scene_ids: List[str] = None) -> str:
        """生成一致性提示词
        
        Args:
            character_ids: 要包含的角色ID列表
            scene_ids: 要包含的场景ID列表
            
        Returns:
            str: 生成的一致性提示词
        """
        prompt_parts = []
        
        # 添加角色一致性提示
        if character_ids:
            characters = self.get_all_characters()
            for char_id in character_ids:
                if char_id in characters:
                    char_data = characters[char_id]
                    if char_data.get("consistency_prompt"):
                        prompt_parts.append(f"角色{char_data['name']}: {char_data['consistency_prompt']}")
        
        # 添加场景一致性提示
        if scene_ids:
            scenes = self.get_all_scenes()
            for scene_id in scene_ids:
                if scene_id in scenes:
                    scene_data = scenes[scene_id]
                    if scene_data.get("consistency_prompt"):
                        prompt_parts.append(f"场景{scene_data['name']}: {scene_data['consistency_prompt']}")
        
        return "; ".join(prompt_parts)
    
    def auto_extract_and_save(self, text: str) -> Dict[str, Any]:
        """自动提取并保存角色和场景信息
        
        Args:
            text: 输入文本
            
        Returns:
            Dict: 提取结果统计
        """
        try:
            # 提取角色
            extracted_characters = self.extract_characters_from_text(text)
            character_count = 0
            for char in extracted_characters:
                char_id = f"auto_{char['name']}_{self._get_current_time().replace(':', '_')}"
                self.save_character(char_id, char)
                character_count += 1
            
            # 提取场景
            extracted_scenes = self.extract_scenes_from_text(text)
            scene_count = 0
            for scene in extracted_scenes:
                scene_id = f"auto_{scene['name']}_{self._get_current_time().replace(':', '_')}"
                self.save_scene(scene_id, scene)
                scene_count += 1
            
            result = {
                "success": True,
                "characters_extracted": character_count,
                "scenes_extracted": scene_count,
                "message": f"成功提取 {character_count} 个角色和 {scene_count} 个场景"
            }
            
            logger.info(f"自动提取完成: {result['message']}")
            return result
            
        except Exception as e:
            logger.error(f"自动提取失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "自动提取失败"
            }
    
    def _get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def export_database(self, export_path: str) -> bool:
        """导出数据库到指定路径
        
        Args:
            export_path: 导出路径
            
        Returns:
            bool: 导出是否成功
        """
        try:
            import shutil
            shutil.copytree(self.database_dir, export_path, dirs_exist_ok=True)
            logger.info(f"数据库已导出到: {export_path}")
            return True
        except Exception as e:
            logger.error(f"导出数据库失败: {e}")
            return False
    
    def import_database(self, import_path: str) -> bool:
        """从指定路径导入数据库
        
        Args:
            import_path: 导入路径
            
        Returns:
            bool: 导入是否成功
        """
        try:
            import shutil
            if os.path.exists(import_path):
                shutil.copytree(import_path, self.database_dir, dirs_exist_ok=True)
                logger.info(f"数据库已从 {import_path} 导入")
                return True
            else:
                logger.error(f"导入路径不存在: {import_path}")
                return False
        except Exception as e:
            logger.error(f"导入数据库失败: {e}")
            return False