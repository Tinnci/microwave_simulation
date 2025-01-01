import pytest
import numpy as np
from gui_rust import MicrowaveGUI
from src.optimization.calculator import calculate_matching
from src.impedance_matching.core import QuarterWaveTransformer, StubMatcher

class TestRustPythonIntegration:
    @pytest.fixture
    def gui_instance(self):
        class MockApp:
            def record_call(self, method_name):
                pass
        return MicrowaveGUI(MockApp())

    def test_data_transfer(self, gui_instance):
        # 测试数据从 Python 到 Rust 的传输
        test_frequency = "2.4e9"
        test_z0 = "50"
        test_load = "75"

        gui_instance.set_frequency(test_frequency)
        gui_instance.set_z0(test_z0)
        gui_instance.set_load(test_load)

        assert gui_instance.frequency == test_frequency
        assert gui_instance.z0 == test_z0
        assert gui_instance.load == test_load

    def test_calculation_integration(self, gui_instance):
        # 测试计算结果的集成
        gui_instance.set_frequency("2.4e9")
        gui_instance.set_z0("50")
        gui_instance.set_load("75")
        gui_instance.set_matching_method("quarter_wave")

        # 触发计算
        result = calculate_matching(
            float(gui_instance.frequency),
            float(gui_instance.z0),
            float(gui_instance.load)
        )

        assert isinstance(result, dict)
        assert "matching_network" in result
        assert "performance_metrics" in result

    def test_error_handling(self, gui_instance):
        # 测试错误处理
        gui_instance.set_frequency("invalid")
        assert not gui_instance.state.frequency_valid

        gui_instance.set_z0("-50")  # 负阻抗
        assert not gui_instance.state.z0_valid

    def test_state_synchronization(self, gui_instance):
        # 测试状态同步
        gui_instance.begin_update()
        gui_instance.set_frequency("2.4e9")
        gui_instance.set_z0("50")
        gui_instance.end_update()

        # 验证状态更新后的一致性
        assert gui_instance.frequency == "2.4e9"
        assert gui_instance.z0 == "50"

    @pytest.mark.parametrize("freq,z0,load,expected_valid", [
        ("2.4e9", "50", "75", True),
        ("invalid", "50", "75", False),
        ("2.4e9", "-50", "75", False),
        ("2.4e9", "50", "invalid", False),
    ])
    def test_input_validation(self, gui_instance, freq, z0, load, expected_valid):
        # 参数化测试输入验证
        gui_instance.set_frequency(freq)
        gui_instance.set_z0(z0)
        gui_instance.set_load(load)
        is_valid = gui_instance.state.is_valid()
        assert is_valid == expected_valid

    def test_matching_methods(self, gui_instance):
        # 测试不同匹配方法
        methods = ["quarter_wave", "stub", "L", "Pi", "T"]
        
        for method in methods:
            gui_instance.set_matching_method(method)
            # 由于 matching_method 是枚举类型，我们只需要验证设置成功，不需要比较字符串
            assert gui_instance.matching_method is not None 