"""
Browser Manager - Handles browser automation using Playwright or Selenium
"""

import time
from typing import Dict, Any, List, Optional, Union
from abc import ABC, abstractmethod

from ..config import get_config
from ..utils.logger import get_logger

logger = get_logger(__name__)

class BaseBrowser(ABC):
    """Abstract base class for browser automation"""
    
    @abstractmethod
    def open(self, url: str) -> None:
        """Open a URL in the browser"""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close the browser"""
        pass
    
    @abstractmethod
    def get_content(self) -> str:
        """Get the current page content"""
        pass
    
    @abstractmethod
    def screenshot(self, path: str) -> None:
        """Take a screenshot of the current page"""
        pass
    
    @abstractmethod
    def click(self, selector: str) -> None:
        """Click on an element"""
        pass
    
    @abstractmethod
    def type(self, selector: str, text: str) -> None:
        """Type text into an element"""
        pass
    
    @abstractmethod
    def evaluate(self, script: str) -> Any:
        """Evaluate JavaScript in the browser"""
        pass


class PlaywrightBrowser(BaseBrowser):
    """Browser automation using Playwright"""
    
    def __init__(self, headless: bool = True):
        """
        Initialize the Playwright browser
        
        Args:
            headless: Whether to run in headless mode
        """
        try:
            from playwright.sync_api import sync_playwright
            
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.firefox.launch(headless=headless)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            self.headless = headless
            
            logger.info("Playwright browser initialized")
            
        except Exception as e:
            logger.error(f"Error initializing Playwright browser: {e}")
            raise
    
    def open(self, url: str) -> None:
        """
        Open a URL in the browser
        
        Args:
            url: The URL to open
        """
        try:
            self.page.goto(url, timeout=get_config("browser.timeout"))
            logger.info(f"Opened URL: {url}")
        except Exception as e:
            logger.error(f"Error opening URL {url}: {e}")
            raise
    
    def close(self) -> None:
        """Close the browser"""
        try:
            self.context.close()
            self.browser.close()
            self.playwright.stop()
            logger.info("Playwright browser closed")
        except Exception as e:
            logger.error(f"Error closing Playwright browser: {e}")
    
    def get_content(self) -> str:
        """
        Get the current page content
        
        Returns:
            The HTML content of the current page
        """
        try:
            return self.page.content()
        except Exception as e:
            logger.error(f"Error getting page content: {e}")
            return ""
    
    def screenshot(self, path: str) -> None:
        """
        Take a screenshot of the current page
        
        Args:
            path: The path to save the screenshot
        """
        try:
            self.page.screenshot(path=path)
            logger.info(f"Screenshot saved to {path}")
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
    
    def click(self, selector: str) -> None:
        """
        Click on an element
        
        Args:
            selector: The CSS selector of the element to click
        """
        try:
            self.page.click(selector)
            logger.info(f"Clicked on element: {selector}")
        except Exception as e:
            logger.error(f"Error clicking on element {selector}: {e}")
            raise
    
    def type(self, selector: str, text: str) -> None:
        """
        Type text into an element
        
        Args:
            selector: The CSS selector of the element to type into
            text: The text to type
        """
        try:
            self.page.fill(selector, text)
            logger.info(f"Typed text into element: {selector}")
        except Exception as e:
            logger.error(f"Error typing into element {selector}: {e}")
            raise
    
    def evaluate(self, script: str) -> Any:
        """
        Evaluate JavaScript in the browser
        
        Args:
            script: The JavaScript to evaluate
            
        Returns:
            The result of the evaluation
        """
        try:
            return self.page.evaluate(script)
        except Exception as e:
            logger.error(f"Error evaluating script: {e}")
            return None


class SeleniumBrowser(BaseBrowser):
    """Browser automation using Selenium"""
    
    def __init__(self, headless: bool = True):
        """
        Initialize the Selenium browser
        
        Args:
            headless: Whether to run in headless mode
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.firefox.options import Options
            
            options = Options()
            if headless:
                options.add_argument("--headless")
                
            self.driver = webdriver.Firefox(options=options)
            self.headless = headless
            
            logger.info("Selenium browser initialized")
            
        except Exception as e:
            logger.error(f"Error initializing Selenium browser: {e}")
            raise
    
    def open(self, url: str) -> None:
        """
        Open a URL in the browser
        
        Args:
            url: The URL to open
        """
        try:
            self.driver.get(url)
            logger.info(f"Opened URL: {url}")
        except Exception as e:
            logger.error(f"Error opening URL {url}: {e}")
            raise
    
    def close(self) -> None:
        """Close the browser"""
        try:
            self.driver.quit()
            logger.info("Selenium browser closed")
        except Exception as e:
            logger.error(f"Error closing Selenium browser: {e}")
    
    def get_content(self) -> str:
        """
        Get the current page content
        
        Returns:
            The HTML content of the current page
        """
        try:
            return self.driver.page_source
        except Exception as e:
            logger.error(f"Error getting page content: {e}")
            return ""
    
    def screenshot(self, path: str) -> None:
        """
        Take a screenshot of the current page
        
        Args:
            path: The path to save the screenshot
        """
        try:
            self.driver.save_screenshot(path)
            logger.info(f"Screenshot saved to {path}")
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
    
    def click(self, selector: str) -> None:
        """
        Click on an element
        
        Args:
            selector: The CSS selector of the element to click
        """
        try:
            from selenium.webdriver.common.by import By
            
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            element.click()
            logger.info(f"Clicked on element: {selector}")
        except Exception as e:
            logger.error(f"Error clicking on element {selector}: {e}")
            raise
    
    def type(self, selector: str, text: str) -> None:
        """
        Type text into an element
        
        Args:
            selector: The CSS selector of the element to type into
            text: The text to type
        """
        try:
            from selenium.webdriver.common.by import By
            
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            element.clear()
            element.send_keys(text)
            logger.info(f"Typed text into element: {selector}")
        except Exception as e:
            logger.error(f"Error typing into element {selector}: {e}")
            raise
    
    def evaluate(self, script: str) -> Any:
        """
        Evaluate JavaScript in the browser
        
        Args:
            script: The JavaScript to evaluate
            
        Returns:
            The result of the evaluation
        """
        try:
            return self.driver.execute_script(script)
        except Exception as e:
            logger.error(f"Error evaluating script: {e}")
            return None


class BrowserManager:
    """
    Manages browser automation using either Playwright or Selenium
    """
    
    def __init__(self, browser_type: Optional[str] = None, headless: Optional[bool] = None):
        """
        Initialize the browser manager
        
        Args:
            browser_type: The type of browser to use ("playwright" or "selenium")
            headless: Whether to run in headless mode
        """
        self.browser_type = browser_type or get_config("browser.type")
        self.headless = headless if headless is not None else get_config("browser.headless")
        self.browser = None
        
    def create_browser(self) -> BaseBrowser:
        """
        Create a browser instance
        
        Returns:
            A browser instance
        """
        if self.browser_type == "playwright":
            return PlaywrightBrowser(headless=self.headless)
        elif self.browser_type == "selenium":
            return SeleniumBrowser(headless=self.headless)
        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")
    
    def get_browser(self) -> BaseBrowser:
        """
        Get the current browser instance or create a new one
        
        Returns:
            A browser instance
        """
        if self.browser is None:
            self.browser = self.create_browser()
            
        return self.browser
    
    def close_browser(self) -> None:
        """Close the current browser instance if it exists"""
        if self.browser is not None:
            self.browser.close()
            self.browser = None
            
    def __enter__(self) -> BaseBrowser:
        """Context manager entry"""
        return self.get_browser()
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit"""
        self.close_browser()