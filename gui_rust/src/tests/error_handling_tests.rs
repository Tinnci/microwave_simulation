use crate::{MicrowaveGUI, Theme, MatchingMethod, ValidationState};
use pyo3::Python;
use super::initialize;

#[test]
fn test_validation_state_transitions() {
    initialize();
    Python::with_gil(|_py| {
        let mut state = ValidationState::default();
        assert!(!state.is_valid());

        state.frequency_valid = true;
        state.z0_valid = true;
        state.load_valid = true;
        assert!(state.is_valid());

        state.frequency_valid = false;
        assert!(!state.is_valid());
    });
}

#[test]
fn test_input_validation_frequency() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 测试有效频率
        gui.set_frequency("2.4e9".to_string());
        assert_eq!(gui.frequency, "2.4e9");
        
        // 测试无效频率
        gui.set_frequency("invalid".to_string());
        assert_eq!(gui.frequency, "2.4e9"); // 应保持旧值
    });
}

#[test]
fn test_input_validation_impedance() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 测试有效阻抗
        gui.set_z0("50".to_string());
        assert_eq!(gui.z0, "50");
        
        // 测试无效阻抗
        gui.set_z0("invalid".to_string());
        assert_eq!(gui.z0, "50"); // 应保持旧值
    });
}

#[test]
fn test_batch_update() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        gui.begin_update();
        gui.set_frequency("2.4e9".to_string());
        gui.set_z0("50".to_string());
        gui.end_update();
        
        assert_eq!(gui.frequency, "2.4e9");
        assert_eq!(gui.z0, "50");
    });
}

#[test]
fn test_matching_method_validation() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 测试有效的匹配方法
        gui.set_matching_method("L");
        assert_eq!(gui.matching_method, MatchingMethod::L);
        
        // 测试无效的匹配方法（应保持旧值）
        gui.set_matching_method("invalid");
        assert_eq!(gui.matching_method, MatchingMethod::L);
    });
}

#[test]
fn test_result_handling() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 测试设置结果
        gui.set_result("test result".to_string());
        assert_eq!(gui.result, "test result");
        
        // 测试清除结果
        gui.clear_result();
        assert_eq!(gui.result, "");
    });
}

#[test]
fn test_complex_state_transitions() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 测试完整的状态转换序列
        gui.begin_update();
        gui.set_frequency("2.4e9".to_string());
        gui.set_z0("50".to_string());
        gui.set_matching_method("L");
        gui.end_update();
        
        assert_eq!(gui.frequency, "2.4e9");
        assert_eq!(gui.z0, "50");
        assert_eq!(gui.matching_method, MatchingMethod::L);
    });
}

#[test]
fn test_error_propagation() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 测试错误传播
        gui.set_error("test error".to_string());
        assert_eq!(gui.error, "test error");
        
        // 测试清除错误
        gui.clear_error();
        assert_eq!(gui.error, "");
    });
}

#[test]
fn test_concurrent_updates() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 测试并发更新
        gui.begin_update();
        gui.set_frequency("2.4e9".to_string());
        gui.set_z0("50".to_string());
        gui.end_update();
        
        gui.begin_update();
        gui.set_matching_method("L");
        gui.set_theme("dark");
        gui.end_update();
        
        assert_eq!(gui.frequency, "2.4e9");
        assert_eq!(gui.z0, "50");
        assert_eq!(gui.matching_method, MatchingMethod::L);
        assert_eq!(gui.theme, Theme::Dark);
    });
}

#[test]
fn test_boundary_conditions() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 测试极大值
        gui.set_frequency("1e20".to_string());
        assert_eq!(gui.frequency, "1e20");
        assert!(gui.state.frequency_valid);
        
        // 测试极小值
        gui.set_frequency("1e-20".to_string());
        assert_eq!(gui.frequency, "1e-20");
        assert!(gui.state.frequency_valid);
        
        // 测试零值
        gui.set_frequency("0".to_string());
        assert_eq!(gui.frequency, "0");
        assert!(gui.state.frequency_valid);
        
        // 测试负值
        gui.set_frequency("-1e9".to_string());
        assert_eq!(gui.frequency, "0"); // 保持上一个有效值
        assert!(!gui.state.frequency_valid);
        
        // 测试阻抗边界条件
        gui.set_z0("0".to_string());
        assert!(!gui.state.z0_valid);
        
        gui.set_z0("1e-20".to_string());
        assert_eq!(gui.z0, "1e-20");
        assert!(gui.state.z0_valid);
        
        // 测试负载边界条件
        gui.set_load("0".to_string());
        assert!(!gui.state.load_valid);
        
        gui.set_load("1e-20".to_string());
        assert_eq!(gui.load, "1e-20");
        assert!(gui.state.load_valid);
    });
}

#[test]
fn test_empty_input() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 测试空字符串
        gui.set_frequency("".to_string());
        assert_eq!(gui.frequency, "");
        assert!(!gui.state.frequency_valid);
        
        // 测试空白字符
        gui.set_frequency(" ".to_string());
        assert_eq!(gui.frequency, "");
        assert!(!gui.state.frequency_valid);
        
        // 测试制表符
        gui.set_frequency("\t".to_string());
        assert_eq!(gui.frequency, "");
        assert!(!gui.state.frequency_valid);
    });
}

#[test]
fn test_special_characters() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 测试特殊字符
        gui.set_frequency("2.4e9!".to_string());
        assert_eq!(gui.frequency, "");
        assert!(!gui.state.frequency_valid);
        
        // 测试Unicode字符
        gui.set_frequency("2.4e9测试".to_string());
        assert_eq!(gui.frequency, "");
        assert!(!gui.state.frequency_valid);
        
        // 测试HTML标签
        gui.set_frequency("<script>2.4e9</script>".to_string());
        assert_eq!(gui.frequency, "");
        assert!(!gui.state.frequency_valid);
    });
}

#[test]
fn test_rapid_updates() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 测试快速连续更新
        for i in 0..1000 {
            gui.set_frequency(format!("{}", i));
            assert_eq!(gui.frequency, format!("{}", i));
            assert!(gui.state.frequency_valid);
        }
    });
}

#[test]
fn test_concurrent_validation() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 测试同时验证多个字段
        gui.begin_update();
        gui.set_frequency("2.4e9".to_string());
        gui.set_z0("50".to_string());
        gui.set_load("75".to_string());
        gui.end_update();
        
        assert!(gui.state.frequency_valid);
        assert!(gui.state.z0_valid);
        assert!(gui.state.load_valid);
        assert!(gui.state.is_valid());
    });
}

#[test]
fn test_validation_state_persistence() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 设置有效值
        gui.set_frequency("2.4e9".to_string());
        assert!(gui.state.frequency_valid);
        
        // 设置无效值
        gui.set_frequency("invalid".to_string());
        assert!(!gui.state.frequency_valid);
        
        // 再次设置有效值
        gui.set_frequency("5.8e9".to_string());
        assert!(gui.state.frequency_valid);
        
        // 验证状态持久性
        assert_eq!(gui.frequency, "5.8e9");
    });
} 