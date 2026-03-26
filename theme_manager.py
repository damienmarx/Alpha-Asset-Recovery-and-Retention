"""
Theme Manager - Dynamic Dashboard Colonization
Manages themes, colors, branding, and UI customization

Features:
- Load and apply themes dynamically
- Generate CSS from theme configuration
- Support user theme preferences
- Custom color palette management
- Branding customization
- Responsive theme switching
"""

import json
import os
from typing import Dict, Optional, List
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class ThemeColors:
    """Theme color palette"""
    primary_color: str
    secondary_color: str
    accent_color: str
    background_color: str
    text_color: str
    border_color: str
    success_color: str
    warning_color: str
    error_color: str
    info_color: str
    header_bg: str
    sidebar_bg: str
    card_bg: str
    input_bg: str
    button_primary: str
    button_hover: str
    button_text: str
    link_color: str
    link_hover: str


class ThemeManager:
    """Manages application themes and branding"""
    
    def __init__(self, config_file: str = "theme_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.current_theme_name = self.config.get("active_theme", "default")
        self.current_theme = self._get_theme(self.current_theme_name)
        self.user_preferences = {}
    
    def _load_config(self) -> Dict:
        """Load theme configuration from JSON file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                print(f"[Theme Manager] Config file not found: {self.config_file}")
                return self._get_default_config()
        except Exception as e:
            print(f"[Theme Manager] Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default configuration if file not found"""
        return {
            "themes": {},
            "active_theme": "default",
            "branding": {},
            "customization": {}
        }
    
    def _get_theme(self, theme_name: str) -> Optional[Dict]:
        """Get theme by name"""
        return self.config.get("themes", {}).get(theme_name)
    
    def list_themes(self) -> List[str]:
        """List all available themes"""
        return list(self.config.get("themes", {}).keys())
    
    def set_theme(self, theme_name: str) -> bool:
        """Set active theme"""
        if theme_name in self.config.get("themes", {}):
            self.current_theme_name = theme_name
            self.current_theme = self._get_theme(theme_name)
            self.config["active_theme"] = theme_name
            self._save_config()
            return True
        else:
            print(f"[Theme Manager] Theme not found: {theme_name}")
            return False
    
    def get_theme_info(self, theme_name: str = None) -> Optional[Dict]:
        """Get theme information"""
        if theme_name is None:
            theme_name = self.current_theme_name
        
        theme = self._get_theme(theme_name)
        if theme:
            return {
                "name": theme.get("name"),
                "description": theme.get("description"),
                "colors": {k: v for k, v in theme.items() 
                          if k not in ["name", "description"]}
            }
        return None
    
    def generate_css(self, theme_name: str = None) -> str:
        """Generate CSS from theme colors"""
        if theme_name is None:
            theme_name = self.current_theme_name
        
        theme = self._get_theme(theme_name)
        if not theme:
            return ""
        
        css = f"""
/* Theme: {theme.get('name')} */
:root {{
    --primary-color: {theme.get('primary_color')};
    --secondary-color: {theme.get('secondary_color')};
    --accent-color: {theme.get('accent_color')};
    --background-color: {theme.get('background_color')};
    --text-color: {theme.get('text_color')};
    --border-color: {theme.get('border_color')};
    --success-color: {theme.get('success_color')};
    --warning-color: {theme.get('warning_color')};
    --error-color: {theme.get('error_color')};
    --info-color: {theme.get('info_color')};
    --header-bg: {theme.get('header_bg')};
    --sidebar-bg: {theme.get('sidebar_bg')};
    --card-bg: {theme.get('card_bg')};
    --input-bg: {theme.get('input_bg')};
    --button-primary: {theme.get('button_primary')};
    --button-hover: {theme.get('button_hover')};
    --button-text: {theme.get('button_text')};
    --link-color: {theme.get('link_color')};
    --link-hover: {theme.get('link_hover')};
}}

body {{
    background-color: var(--background-color);
    color: var(--text-color);
    font-family: {self.config.get('customization', {}).get('default_font', 'Inter, system-ui, sans-serif')};
}}

header {{
    background-color: var(--header-bg);
    border-bottom: 1px solid var(--border-color);
}}

.sidebar {{
    background-color: var(--sidebar-bg);
    border-right: 1px solid var(--border-color);
}}

.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: {self.config.get('customization', {}).get('border_radius', '8px')};
    padding: {self.config.get('dashboard_layout', {}).get('card_padding', '20px')};
}}

input, textarea, select {{
    background-color: var(--input-bg);
    color: var(--text-color);
    border: 1px solid var(--border-color);
    border-radius: {self.config.get('customization', {}).get('border_radius', '8px')};
}}

button.btn-primary {{
    background-color: var(--button-primary);
    color: var(--button-text);
    border: none;
    border-radius: {self.config.get('customization', {}).get('border_radius', '8px')};
    cursor: pointer;
    transition: background-color {self.config.get('customization', {}).get('transition_speed', '300ms')};
}}

button.btn-primary:hover {{
    background-color: var(--button-hover);
}}

a {{
    color: var(--link-color);
    text-decoration: none;
    transition: color {self.config.get('customization', {}).get('transition_speed', '300ms')};
}}

a:hover {{
    color: var(--link-hover);
}}

.alert-success {{
    background-color: var(--success-color);
    color: white;
}}

.alert-warning {{
    background-color: var(--warning-color);
    color: white;
}}

.alert-error {{
    background-color: var(--error-color);
    color: white;
}}

.alert-info {{
    background-color: var(--info-color);
    color: white;
}}

.badge-primary {{
    background-color: var(--primary-color);
    color: white;
}}

.badge-accent {{
    background-color: var(--accent-color);
    color: white;
}}

.progress-bar {{
    background-color: var(--primary-color);
}}

.table {{
    border-color: var(--border-color);
}}

.table tbody tr {{
    border-bottom: 1px solid var(--border-color);
}}

.table tbody tr:hover {{
    background-color: var(--card-bg);
}}

.form-group label {{
    color: var(--text-color);
}}

.divider {{
    border-color: var(--border-color);
}}

/* Responsive Design */
@media (max-width: 768px) {{
    .sidebar {{
        width: 100%;
        border-right: none;
        border-bottom: 1px solid var(--border-color);
    }}
    
    .card {{
        margin-bottom: 10px;
    }}
}}
"""
        return css
    
    def save_css_file(self, output_file: str = "static/css/theme.css", theme_name: str = None) -> bool:
        """Save generated CSS to file"""
        try:
            css = self.generate_css(theme_name)
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w') as f:
                f.write(css)
            print(f"[Theme Manager] CSS saved to {output_file}")
            return True
        except Exception as e:
            print(f"[Theme Manager] Error saving CSS: {e}")
            return False
    
    def get_branding(self) -> Dict:
        """Get branding information"""
        return self.config.get("branding", {})
    
    def set_branding(self, branding_data: Dict) -> bool:
        """Update branding information"""
        try:
            self.config["branding"].update(branding_data)
            self._save_config()
            return True
        except Exception as e:
            print(f"[Theme Manager] Error updating branding: {e}")
            return False
    
    def get_customization(self) -> Dict:
        """Get customization settings"""
        return self.config.get("customization", {})
    
    def set_customization(self, customization_data: Dict) -> bool:
        """Update customization settings"""
        try:
            self.config["customization"].update(customization_data)
            self._save_config()
            return True
        except Exception as e:
            print(f"[Theme Manager] Error updating customization: {e}")
            return False
    
    def create_custom_theme(self, theme_name: str, colors: Dict, 
                           description: str = "") -> bool:
        """Create a custom theme"""
        try:
            if theme_name in self.config.get("themes", {}):
                print(f"[Theme Manager] Theme already exists: {theme_name}")
                return False
            
            custom_theme = {
                "name": theme_name,
                "description": description,
                **colors
            }
            
            if "themes" not in self.config:
                self.config["themes"] = {}
            
            self.config["themes"][theme_name] = custom_theme
            self._save_config()
            print(f"[Theme Manager] Custom theme created: {theme_name}")
            return True
        except Exception as e:
            print(f"[Theme Manager] Error creating custom theme: {e}")
            return False
    
    def export_theme(self, theme_name: str, output_file: str) -> bool:
        """Export theme to JSON file"""
        try:
            theme = self._get_theme(theme_name)
            if not theme:
                return False
            
            with open(output_file, 'w') as f:
                json.dump(theme, f, indent=2)
            print(f"[Theme Manager] Theme exported to {output_file}")
            return True
        except Exception as e:
            print(f"[Theme Manager] Error exporting theme: {e}")
            return False
    
    def import_theme(self, input_file: str, theme_name: str = None) -> bool:
        """Import theme from JSON file"""
        try:
            with open(input_file, 'r') as f:
                theme_data = json.load(f)
            
            if theme_name is None:
                theme_name = theme_data.get("name", "imported_theme")
            
            if "themes" not in self.config:
                self.config["themes"] = {}
            
            self.config["themes"][theme_name] = theme_data
            self._save_config()
            print(f"[Theme Manager] Theme imported: {theme_name}")
            return True
        except Exception as e:
            print(f"[Theme Manager] Error importing theme: {e}")
            return False
    
    def get_color_presets(self) -> List[Dict]:
        """Get available color presets"""
        return self.config.get("color_presets", [])
    
    def apply_color_preset(self, preset_name: str, theme_name: str = None) -> bool:
        """Apply color preset to theme"""
        try:
            if theme_name is None:
                theme_name = self.current_theme_name
            
            theme = self._get_theme(theme_name)
            if not theme:
                return False
            
            presets = {p["name"]: p for p in self.get_color_presets()}
            if preset_name not in presets:
                return False
            
            preset = presets[preset_name]
            theme["primary_color"] = preset.get("primary")
            theme["secondary_color"] = preset.get("secondary")
            theme["accent_color"] = preset.get("accent")
            
            self._save_config()
            return True
        except Exception as e:
            print(f"[Theme Manager] Error applying preset: {e}")
            return False
    
    def get_dashboard_layout(self) -> Dict:
        """Get dashboard layout configuration"""
        return self.config.get("dashboard_layout", {})
    
    def _save_config(self) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"[Theme Manager] Error saving config: {e}")
            return False
    
    def get_full_config(self) -> Dict:
        """Get full configuration"""
        return self.config
    
    def get_theme_stats(self) -> Dict:
        """Get theme statistics"""
        return {
            "total_themes": len(self.config.get("themes", {})),
            "active_theme": self.current_theme_name,
            "available_themes": self.list_themes(),
            "color_presets": len(self.get_color_presets()),
            "customization_enabled": self.config.get("customization", {}).get("enable_custom_colors", False),
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=== THEME MANAGER ===\n")
    
    # Initialize theme manager
    manager = ThemeManager("theme_config.json")
    
    # List available themes
    print("Available Themes:")
    for theme in manager.list_themes():
        print(f"  - {theme}")
    print()
    
    # Get current theme info
    print(f"Current Theme: {manager.current_theme_name}")
    theme_info = manager.get_theme_info()
    if theme_info:
        print(f"Name: {theme_info['name']}")
        print(f"Description: {theme_info['description']}\n")
    
    # Generate CSS
    print("Generating CSS...")
    manager.save_css_file()
    print()
    
    # Get branding
    print("Branding:")
    branding = manager.get_branding()
    for key, value in branding.items():
        print(f"  {key}: {value}")
    print()
    
    # Get theme stats
    print("Theme Statistics:")
    stats = manager.get_theme_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()
    
    # Switch theme
    print("Switching to 'alpha_recovery' theme...")
    if manager.set_theme("alpha_recovery"):
        print(f"Active theme: {manager.current_theme_name}")
        manager.save_css_file()
    print()
    
    # Create custom theme
    print("Creating custom theme...")
    custom_colors = {
        "primary_color": "#ff0000",
        "secondary_color": "#ff6600",
        "accent_color": "#ffff00",
        "background_color": "#1a1a1a",
        "text_color": "#ffffff",
        "border_color": "#333333",
        "success_color": "#00ff00",
        "warning_color": "#ffff00",
        "error_color": "#ff0000",
        "info_color": "#00ffff",
        "header_bg": "#1a1a1a",
        "sidebar_bg": "#0d0d0d",
        "card_bg": "#262626",
        "input_bg": "#1a1a1a",
        "button_primary": "#ff0000",
        "button_hover": "#ff6600",
        "button_text": "#ffffff",
        "link_color": "#00ffff",
        "link_hover": "#00ff00"
    }
    
    if manager.create_custom_theme("custom_red", custom_colors, "Custom red theme"):
        print("Custom theme created successfully")
        manager.set_theme("custom_red")
        manager.save_css_file()
