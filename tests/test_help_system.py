"""帮助系统测试"""
import pytest
from src.help.help_system import HelpSystem

class TestHelpSystem:
    """测试帮助系统类"""
    
    @pytest.fixture
    def help_system(self):
        """创建帮助系统实例"""
        return HelpSystem()
        
    def test_init(self, help_system):
        """测试初始化"""
        # 测试工具提示字典
        assert isinstance(help_system.tooltips, dict)
        assert len(help_system.tooltips) > 0
        assert "freq" in help_system.tooltips
        assert "z0" in help_system.tooltips
        assert "z_load_real" in help_system.tooltips
        assert "z_load_imag" in help_system.tooltips
        assert "matching_method" in help_system.tooltips
        
        # 测试帮助内容字典
        assert isinstance(help_system.help_content, dict)
        assert len(help_system.help_content) > 0
        assert "quarter_wave" in help_system.help_content
        assert "stub" in help_system.help_content
        
    def test_get_tooltip(self, help_system):
        """测试获取工具提示"""
        # 测试有效字段
        assert help_system.get_tooltip("freq") == "工作频率 (Hz)"
        assert help_system.get_tooltip("z0") == "特征阻抗 (Ω)"
        assert help_system.get_tooltip("z_load_real") == "负载阻抗实部 (Ω)"
        assert help_system.get_tooltip("z_load_imag") == "负载阻抗虚部 (Ω)"
        assert help_system.get_tooltip("matching_method") == "匹配方法选择"
        
        # 测试无效字段
        assert help_system.get_tooltip("invalid") == ""
        assert help_system.get_tooltip("") == ""
        assert help_system.get_tooltip(None) == ""
        
    def test_get_help_content(self, help_system):
        """测试获取帮助内容"""
        # 测试四分之一波长变换器
        quarter_wave_help = help_system.get_help_content("quarter_wave")
        assert "四分之一波长变换器" in quarter_wave_help
        assert "原理" in quarter_wave_help
        assert "参数" in quarter_wave_help
        assert "频率" in quarter_wave_help
        assert "特征阻抗" in quarter_wave_help
        assert "负载阻抗" in quarter_wave_help
        
        # 测试单枝节匹配器
        stub_help = help_system.get_help_content("stub")
        assert "单枝节匹配器" in stub_help
        assert "原理" in stub_help
        assert "参数" in stub_help
        assert "频率" in stub_help
        assert "特征阻抗" in stub_help
        assert "负载阻抗" in stub_help
        
        # 测试无效主题
        assert help_system.get_help_content("invalid") == ""
        assert help_system.get_help_content("") == ""
        assert help_system.get_help_content(None) == ""
        
    def test_tooltip_content(self, help_system):
        """测试工具提示内容"""
        # 测试每个工具提示的内容格式
        for field, tooltip in help_system.tooltips.items():
            assert isinstance(field, str)
            assert isinstance(tooltip, str)
            assert len(tooltip) > 0
            
    def test_help_content_format(self, help_system):
        """测试帮助内容格式"""
        # 测试每个帮助内容的格式
        for topic, content in help_system.help_content.items():
            assert isinstance(topic, str)
            assert isinstance(content, str)
            assert len(content) > 0
            assert "原理" in content
            assert "参数" in content 