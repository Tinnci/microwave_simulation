use crate::{MicrowaveGUI, Theme};
use pyo3::Python;
use super::initialize;

#[test]
fn test_theme_default() {
    initialize();
    Python::with_gil(|_py| {
        assert_eq!(Theme::default(), Theme::Light);
    });
}

#[test]
fn test_theme_switching() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        assert_eq!(gui.theme, Theme::Light);
        
        gui.set_theme("dark");
        assert_eq!(gui.theme, Theme::Dark);
        
        gui.set_theme("light");
        assert_eq!(gui.theme, Theme::Light);
    });
}

#[test]
fn test_theme_invalid_value() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        assert_eq!(gui.theme, Theme::Light);
        
        // 测试无效的主题值（应该默认为 Light）
        gui.set_theme("invalid");
        assert_eq!(gui.theme, Theme::Light);
    });
}

#[test]
fn test_theme_persistence() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 测试主题设置的持久性
        gui.set_theme("dark");
        assert_eq!(gui.theme, Theme::Dark);
        
        // 执行其他操作不应影响主题
        gui.set_frequency("2.4e9".to_string());
        gui.set_z0("50".to_string());
        assert_eq!(gui.theme, Theme::Dark);
    });
}

#[test]
fn test_theme_batch_update() {
    initialize();
    Python::with_gil(|_py| {
        let mut gui = MicrowaveGUI::default();
        
        // 在批量更新中切换主题
        gui.begin_update();
        gui.set_theme("dark");
        gui.set_frequency("2.4e9".to_string());
        gui.end_update();
        
        assert_eq!(gui.theme, Theme::Dark);
        assert_eq!(gui.frequency, "2.4e9");
    });
} 