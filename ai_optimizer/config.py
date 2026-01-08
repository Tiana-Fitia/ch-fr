# -*- coding: utf-8 -*-
"""
Configuration - Configuration Module
Configuration management for AI Optimizer
"""

import logging

logger = logging.getLogger(__name__)

class Config:
    """Configuration manager"""
    
    def __init__(self, config_path=None):
        """Initialize configuration"""
        # Configuration par defaut
        self.config = {
            'target_column': 'target',
            'test_size': 0.2,
            'random_state': 42,
            'optimization': {
                'n_trials': 20,
                'cv_folds': 5,
                'scoring': 'accuracy'
            },
            'models': {
                'random_forest': {
                    'enabled': True,
                    'n_estimators_range': [100, 200, 300],
                    'max_depth_range': [3, 5, 7, 10, None]
                },
                'gradient_boosting': {
                    'enabled': True,
                    'n_estimators_range': [100, 200],
                    'learning_rate_range': [0.01, 0.1, 0.3]
                }
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        }
        
        logger.info("Using default configuration")
    
    def get(self, key, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key, value):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def validate(self):
        """Validate configuration"""
        return True
    
    def to_dict(self):
        """Return configuration as dictionary"""
        return self.config.copy()
