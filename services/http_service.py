import requests
import logging
from typing import Dict, Any, Optional
from requests.exceptions import RequestException, Timeout, HTTPError

class HttpService:
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """
        Initialize HTTP Service
        
        Args:
            timeout (int): Request timeout in seconds
            max_retries (int): Maximum number of retries for failed requests
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'CitiBikes-DataPipeline/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        self.logger.info(f"HTTP Service initialized with timeout: {timeout}s, max retries: {max_retries}")
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make HTTP request with retry logic and error handling
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE, PATCH)
            url (str): Target URL
            **kwargs: Additional request parameters
            
        Returns:
            requests.Response: HTTP response object
            
        Raises:
            RequestException: For request-related errors
            HTTPError: For HTTP error responses
        """
        for attempt in range(self.max_retries + 1):
            try:
                self.logger.debug(f"Making {method} request to {url} (attempt {attempt + 1})")
                
                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs
                )
                
                # Raise exception for bad status codes
                response.raise_for_status()
                
                self.logger.info(f"Successful {method} request to {url} - Status: {response.status_code}")
                return response
                
            except Timeout:
                if attempt < self.max_retries:
                    self.logger.warning(f"Request timeout, retrying... (attempt {attempt + 1}/{self.max_retries + 1})")
                    continue
                else:
                    self.logger.error(f"Request to {url} timed out after {self.max_retries + 1} attempts")
                    raise Timeout(f"Request to {url} timed out after {self.max_retries + 1} attempts")
                    
            except HTTPError as e:
                self.logger.error(f"HTTP error {e.response.status_code} for {method} request to {url}")
                raise
                
            except RequestException as e:
                if attempt < self.max_retries:
                    self.logger.warning(f"Request failed, retrying... (attempt {attempt + 1}/{self.max_retries + 1}): {e}")
                    continue
                else:
                    self.logger.error(f"Request to {url} failed after {self.max_retries + 1} attempts: {e}")
                    raise
        
        raise RequestException(f"Request to {url} failed after {self.max_retries + 1} attempts")
    
    def get(self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """
        Make GET request
        
        Args:
            url (str): Target URL
            params (Optional[Dict[str, Any]]): Query parameters
            **kwargs: Additional request parameters
            
        Returns:
            requests.Response: HTTP response object
        """
        return self._make_request('GET', url, params=params, **kwargs)
    
    def post(self, url: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """
        Make POST request
        
        Args:
            url (str): Target URL
            data (Optional[Dict[str, Any]]): Form data
            json_data (Optional[Dict[str, Any]]): JSON data
            **kwargs: Additional request parameters
            
        Returns:
            requests.Response: HTTP response object
        """
        kwargs.update({'data': data, 'json': json_data})
        return self._make_request('POST', url, **kwargs)
    
    def put(self, url: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """
        Make PUT request
        
        Args:
            url (str): Target URL
            data (Optional[Dict[str, Any]]): Form data
            json_data (Optional[Dict[str, Any]]): JSON data
            **kwargs: Additional request parameters
            
        Returns:
            requests.Response: HTTP response object
        """
        kwargs.update({'data': data, 'json': json_data})
        return self._make_request('PUT', url, **kwargs)
    
    def patch(self, url: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """
        Make PATCH request
        
        Args:
            url (str): Target URL
            data (Optional[Dict[str, Any]]): Form data
            json_data (Optional[Dict[str, Any]]): JSON data
            **kwargs: Additional request parameters
            
        Returns:
            requests.Response: HTTP response object
        """
        kwargs.update({'data': data, 'json': json_data})
        return self._make_request('PATCH', url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> requests.Response:
        """
        Make DELETE request
        
        Args:
            url (str): Target URL
            **kwargs: Additional request parameters
            
        Returns:
            requests.Response: HTTP response object
        """
        return self._make_request('DELETE', url, **kwargs)
    
    def config_service(self, headers: Dict[str, str]) -> 'HttpService':
        """
        Configure service headers
        
        Args:
            headers (Dict[str, str]): Headers to add/update
            
        Returns:
            HttpService: Self for method chaining
        """
        self.session.headers.update(headers)
        self.logger.info(f"Updated service headers: {headers}")
        return self
    
    def set_auth(self, auth_type: str, **auth_params) -> 'HttpService':
        """
        Set authentication for requests
        
        Args:
            auth_type (str): Type of authentication ('basic', 'bearer', 'api_key')
            **auth_params: Authentication parameters
            
        Returns:
            HttpService: Self for method chaining
        """
        if auth_type == 'basic':
            from requests.auth import HTTPBasicAuth
            username = auth_params.get('username')
            password = auth_params.get('password')
            if username and password:
                self.session.auth = HTTPBasicAuth(username, password)
                self.logger.info("Basic authentication configured")
                
        elif auth_type == 'bearer':
            token = auth_params.get('token')
            if token:
                self.session.headers.update({'Authorization': f'Bearer {token}'})
                self.logger.info("Bearer token authentication configured")
                
        elif auth_type == 'api_key':
            key_name = auth_params.get('key_name', 'X-API-Key')
            key_value = auth_params.get('key_value')
            if key_value:
                self.session.headers.update({key_name: key_value})
                self.logger.info(f"API key authentication configured with header: {key_name}")
        
        return self
    
    def close(self):
        """Close the HTTP session"""
        try:
            self.session.close()
            self.logger.info("HTTP session closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing HTTP session: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

    
