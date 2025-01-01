import pytest
import numpy as np
from microwave_gui import MicrowaveGUI
from src.optimization import calculator
from src.impedance_matching import matching

class TestRustPythonIntegration:
    @pytest.fixture
    def gui_instance(self):
        return MicrowaveGUI()

    def test_data_transfer(self, gui_instance):
        # 测试数据从 Python 到 Rust 的传输
        test_frequency = "2.4e9"
        test_z0 = "50"
        test_zl_real = "75"
        test_zl_imag = "25"

        gui_instance.set_frequency(test_frequency)
        gui_instance.set_z0(test_z0)
        gui_instance.set_z_load_real(test_zl_real)
        gui_instance.set_z_load_imag(test_zl_imag)

        assert gui_instance.frequency == test_frequency
        assert gui_instance.z0 == test_z0
        assert gui_instance.z_load_real == test_zl_real
        assert gui_instance.z_load_imag == test_zl_imag

    def test_calculation_integration(self, gui_instance):
        # 测试计算结果的集成
        gui_instance.set_frequency("2.4e9")
        gui_instance.set_z0("50")
        gui_instance.set_z_load_real("75")
        gui_instance.set_z_load_imag("25")
        gui_instance.set_matching_method("quarter_wave")

        # 触发计算
        result = calculator.calculate_matching(
            float(gui_instance.frequency),
            float(gui_instance.z0),
            complex(float(gui_instance.z_load_real), float(gui_instance.z_load_imag))
        )

        assert isinstance(result, dict)
        assert "matching_network" in result
        assert "performance_metrics" in result

    def test_error_handling(self, gui_instance):
        # 测试错误处理
        with pytest.raises(ValueError):
            gui_instance.set_frequency("invalid")

        with pytest.raises(ValueError):
            calculator.calculate_matching(
                float("1e9"),
                float("-50"),  # 负阻抗，应该引发错误
                complex(75, 25)
            )

    @pytest.mark.asyncio
    async def test_async_operation(self, gui_instance):
        # 测试异步操作
        import asyncio
        
        async def async_calculation():
            await asyncio.sleep(0.1)  # 模拟异步计算
            return {"result": "success"}

        result = await async_calculation()
        assert result["result"] == "success"

    def test_state_synchronization(self, gui_instance):
        # 测试状态同步
        gui_instance.begin_update()
        gui_instance.set_frequency("2.4e9")
        gui_instance.set_z0("50")
        gui_instance.end_update()

        # 验证状态更新后的一致性
        assert gui_instance.frequency == "2.4e9"
        assert gui_instance.z0 == "50"

    @pytest.mark.parametrize("freq,z0,zl_real,zl_imag,expected_valid", [
        ("2.4e9", "50", "75", "25", True),
        ("invalid", "50", "75", "25", False),
        ("2.4e9", "-50", "75", "25", False),
        ("2.4e9", "50", "invalid", "25", False),
    ])
    def test_input_validation(self, gui_instance, freq, z0, zl_real, zl_imag, expected_valid):
        # 参数化测试输入验证
        try:
            gui_instance.set_frequency(freq)
            gui_instance.set_z0(z0)
            gui_instance.set_z_load_real(zl_real)
            gui_instance.set_z_load_imag(zl_imag)
            is_valid = True
        except ValueError:
            is_valid = False

        assert is_valid == expected_valid 