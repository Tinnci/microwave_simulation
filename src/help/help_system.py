"""帮助系统模块"""

class HelpSystem:
    """帮助系统类"""
    
    def __init__(self):
        """初始化帮助系统"""
        self.tooltips = {
            "freq": "工作频率 (Hz)",
            "z0": "特征阻抗 (Ω)",
            "z_load_real": "负载阻抗实部 (Ω)",
            "z_load_imag": "负载阻抗虚部 (Ω)",
            "matching_method": "匹配方法选择"
        }
        
        self.help_content = {
            "quarter_wave": """
            四分之一波长变换器
            
            原理：
            利用四分之一波长传输线实现阻抗匹配。
            
            参数：
            - 频率：工作频率
            - 特征阻抗：传输线特征阻抗
            - 负载阻抗：待匹配负载的复数阻抗
            """,
            
            "stub": """
            单枝节匹配器
            
            原理：
            利用并联短路支节实现阻抗匹配。
            
            参数：
            - 频率：工作频率
            - 特征阻抗：传输线特征阻抗
            - 负载阻抗：待匹配负载的复数阻抗
            """
        }
        
    def get_tooltip(self, field):
        """
        获取工具提示

        参数:
            field: str, 字段名称

        返回:
            str, 工具提示文本
        """
        return self.tooltips.get(field, "")
        
    def get_help_content(self, topic):
        """
        获取帮助内容

        参数:
            topic: str, 主题名称

        返回:
            str, 帮助内容文本
        """
        return self.help_content.get(topic, "") 