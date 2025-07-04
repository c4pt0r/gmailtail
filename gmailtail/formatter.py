"""
Output formatting for gmailtail
"""

import json
import sys
from typing import Dict, Any, List, Optional

from .config import Config


class OutputFormatter:
    """Handle different output formats for email messages"""
    
    def __init__(self, config: Config):
        self.config = config
    
    def format_message(self, message: Dict[str, Any]) -> str:
        """Format a single message according to the configured output format"""
        # Filter fields if specified
        if self.config.output.fields:
            filtered_message = {}
            for field in self.config.output.fields:
                if field in message:
                    filtered_message[field] = message[field]
            message = filtered_message
        
        # Format according to output format
        if self.config.output.format == 'json':
            return self._format_json(message)
        elif self.config.output.format == 'json-lines':
            return self._format_json_lines(message)
        elif self.config.output.format == 'compact':
            return self._format_compact(message)
        else:
            return self._format_json(message)
    
    def _format_json(self, message: Dict[str, Any]) -> str:
        """Format as pretty JSON"""
        if self.config.output.pretty:
            return json.dumps(message, indent=2, ensure_ascii=False)
        else:
            return json.dumps(message, ensure_ascii=False)
    
    def _format_json_lines(self, message: Dict[str, Any]) -> str:
        """Format as JSON Lines (one JSON object per line)"""
        return json.dumps(message, ensure_ascii=False)
    
    def _format_compact(self, message: Dict[str, Any]) -> str:
        """Format as compact single-line representation"""
        timestamp = message.get('timestamp', 'unknown')
        subject = message.get('subject', 'No subject')
        from_addr = message.get('from', {})
        from_email = from_addr.get('email', 'unknown') if isinstance(from_addr, dict) else str(from_addr)
        
        # Truncate subject if too long
        if len(subject) > 50:
            subject = subject[:47] + "..."
        
        return f"{timestamp} | {from_email} | {subject}"
    
    def output_message(self, message: Dict[str, Any]):
        """Output a formatted message to stdout"""
        formatted = self.format_message(message)
        print(formatted)
        sys.stdout.flush()
    
    def output_error(self, error: str):
        """Output an error message to stderr"""
        if not self.config.quiet:
            print(f"Error: {error}", file=sys.stderr)
    
    def output_info(self, info: str):
        """Output an info message to stderr (if not quiet)"""
        if not self.config.quiet:
            print(info, file=sys.stderr)
    
    def output_verbose(self, info: str):
        """Output a verbose message to stderr (if verbose mode)"""
        if self.config.verbose:
            print(f"[VERBOSE] {info}", file=sys.stderr)