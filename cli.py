# #!/usr/bin/env python3
# """
# Command Line Interface for Secret Manager
# Provides a comprehensive CLI tool for managing secrets
# """
#
# import argparse
# import sys
# import os
# from getpass import getpass
# from tabulate import tabulate
# from colorama import init, Fore, Back, Style
# from secret_manager import SecretManager, SecretManagerCLI
#
# # Initialize colorama for cross-platform colored terminal text
# init(autoreset=True)
#
#
# def print_banner():
#     """Print application banner"""
#     banner = f"""
# {Fore.CYAN}╔══════════════════════════════════════════════════════════╗
# ║                    🔐 SECRET MANAGER 🔐                   ║
# ║              Secure Storage & Retrieval System            ║
# ╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
# """
#     print(banner)
#
#
# def print_success(message):
#     """Print success message in green"""
#     print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
#
#
# def print_error(message):
#     """Print error message in red"""
#     print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")
#
#
# def print_info(message):
#     """Print info message in blue"""
#     print(f"{Fore.BLUE}ℹ️  {message}{Style.RESET_ALL}")
#
#
# def print_warning(message):
#     """Print warning message in yellow"""
#     print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")
#
#
# class SecretManagerAdvancedCLI:
#     """Advanced CLI with enhanced features"""
#
#     def __init__(self):
#         self.manager = None
#         self.storage_file = "secrets.dat"
#
#     def setup_manager(self, master_key=None, storage_file=None):
#         """Setup the secret manager"""
#         if storage_file:
#             self.storage_file = storage_file
#
#         try:
#             self.manager = SecretManager(self.storage_file, master_key)
#             print_success(f"Secret Manager initialized with storage: {self.storage_file}")
#             return True
#         except Exception as e:
#             print_error(f"Failed to initialize Secret Manager: {e}")
#             return False
#
#     def store_secret(self, args):
#         """Store a new secret"""
#         if not self.manager:
#             print_error("Secret Manager not initialized")
#             return
#
#         name = args.name
#         description = args.description or ""
#         tags = args.tags.split(",") if args.tags else []
#
#         # Clean up tags
#         tags = [tag.strip() for tag in tags if tag.strip()]
#
#         try:
#             ref = self.manager.store_secret(name, description, tags)
#             print_success(f"Secret '{name}' stored successfully")
#             print_info(f"Reference ID: {ref}")
#
#             if args.verbose:
#                 print(f"\n{Fore.CYAN}Secret Details:{Style.RESET_ALL}")
#                 print(f"  Name: {name}")
#                 print(f"  Description: {description}")
#                 print(f"  Tags: {', '.join(tags) if tags else 'None'}")
#                 print(f"  Reference: {ref}")
#
#         except Exception as e:
#             print_error(f"Error storing secret: {e}")
#
#     def retrieve_secret(self, args):
#         """Retrieve a secret"""
#         if not self.manager:
#             print_error("Secret Manager not initialized")
#             return
#
#         secret = self.manager.retrieve_secret(args.name)
#
#         if not secret:
#             print_error(f"Secret '{args.name}' not found")
#             return
#
#         print_success(f"Secret '{args.name}' retrieved")
#
#         # Display in table format
#         data = [
#             ["Name", secret['name']],
#             ["Description", secret['description'] or "No description"],
#             ["Tags", ', '.join(secret['tags']) if secret['tags'] else "None"],
#             ["Reference", secret['reference']],
#             ["Created", secret['created_at']],
#             ["Last Accessed", secret['last_accessed'] or "Never"],
#             ["Access Count", secret['access_count']],
#         ]
#
#         if not args.no_value:
#             data.append(["Simulated Value", secret['simulated_value']])
#
#         print(f"\n{tabulate(data, headers=['Property', 'Value'], tablefmt='grid')}")
#
#     def list_secrets(self, args):
#         """List all secrets"""
#         if not self.manager:
#             print_error("Secret Manager not initialized")
#             return
#
#         secrets = self.manager.list_secrets(args.tag)
#
#         if not secrets:
#             print_warning("No secrets found")
#             return
#
#         print_info(f"Found {len(secrets)} secrets")
#
#         if args.format == 'table':
#             # Table format
#             table_data = []
#             for secret in secrets:
#                 table_data.append([
#                     secret['name'],
#                     secret['description'][:30] + "..." if len(secret['description']) > 30 else secret['description'],
#                     ', '.join(secret['tags'][:2]) + "..." if len(secret['tags']) > 2 else ', '.join(secret['tags']),
#                     secret['access_count'],
#                     secret['created_at'][:10]  # Just the date
#                 ])
#
#             headers = ['Name', 'Description', 'Tags', 'Accesses', 'Created']
#             print(f"\n{tabulate(table_data, headers=headers, tablefmt='grid')}")
#
#         else:
#             # Detailed format
#             print()
#             for i, secret in enumerate(secrets, 1):
#                 print(f"{Fore.CYAN}[{i}] {secret['name']}{Style.RESET_ALL}")
#                 print(f"    Description: {secret['description'] or 'No description'}")
#                 print(f"    Tags: {', '.join(secret['tags']) if secret['tags'] else 'None'}")
#                 print(f"    Created: {secret['created_at']}")
#                 print(f"    Accesses: {secret['access_count']}")
#                 print()
#
#     def update_secret(self, args):
#         """Update secret metadata"""
#         if not self.manager:
#             print_error("Secret Manager not initialized")
#             return
#
#         tags = args.tags.split(",") if args.tags else None
#         if tags:
#             tags = [tag.strip() for tag in tags if tag.strip()]
#
#         success = self.manager.update_secret(args.name, args.description, tags)
#
#         if success:
#             print_success(f"Secret '{args.name}' updated successfully")
#         else:
#             print_error(f"Secret '{args.name}' not found")
#
#     def delete_secret(self, args):
#         """Delete a secret"""
#         if not self.manager:
#             print_error("Secret Manager not initialized")
#             return
#
#         if not args.force:
#             confirm = input(f"Are you sure you want to delete secret '{args.name}'? (y/N): ")
#             if confirm.lower() != 'y':
#                 print_info("Deletion cancelled")
#                 return
#
#         success = self.manager.delete_secret(args.name)
#
#         if success:
#             print_success(f"Secret '{args.name}' deleted successfully")
#         else:
#             print_error(f"Secret '{args.name}' not found")
#
#     def rotate_secret(self, args):
#         """Rotate a secret"""
#         if not self.manager:
#             print_error("Secret Manager not initialized")
#             return
#
#         new_ref = self.manager.rotate_secret(args.name)
#
#         if new_ref:
#             print_success(f"Secret '{args.name}' rotated successfully")
#             print_info(f"New reference ID: {new_ref}")
#         else:
#             print_error(f"Secret '{args.name}' not found")
#
#     def show_stats(self, args):
#         """Show statistics"""
#         if not self.manager:
#             print_error("Secret Manager not initialized")
#             return
#
#         stats = self.manager.get_secret_stats()
#
#         print(f"\n{Fore.CYAN}📊 Secret Manager Statistics{Style.RESET_ALL}")
#         print("=" * 40)
#
#         stats_data = [
#             ["Total Secrets", stats['total_secrets']],
#             ["Total Accesses", stats['total_accesses']],
#             ["Recent Activity (24h)", stats['recent_activity']],
#         ]
#
#         if stats['most_accessed']:
#             stats_data.append(["Most Accessed",
#                                f"{stats['most_accessed']['name']} ({stats['most_accessed']['access_count']} times)"])
#
#         print(tabulate(stats_data, headers=['Metric', 'Value'], tablefmt='grid'))
#
#     def show_audit_log(self, args):
#         """Show audit log"""
#         if not self.manager:
#             print_error("Secret Manager not initialized")
#             return
#
#         logs = self.manager.get_audit_log(args.limit)
#
#         if not logs:
#             print_warning("No audit log entries found")
#             return
#
#         print_info(f"Showing last {len(logs)} audit log entries")
#
#         log_data = []
#         for log in logs:
#             status = "✅" if log['success'] else "❌"
#             log_data.append([
#                 log['timestamp'][:19],  # Remove microseconds
#                 log['action'],
#                 log['secret_name'],
#                 status,
#                 log['session_id']
#             ])
#
#         headers = ['Timestamp', 'Action', 'Secret Name', 'Status', 'Session']
#         print(f"\n{tabulate(log_data, headers=headers, tablefmt='grid')}")
#
#
# def main():
#     """Main CLI function"""
#     parser = argparse.ArgumentParser(
#         description="Secret Manager - Secure storage and retrieval of application secrets",
#         formatter_class=argparse.RawDescriptionHelpFormatter,
#         epilog="""
# Examples:
#   %(prog)s store my_api_key --description "Production API key" --tags "api,production"
#   %(prog)s retrieve my_api_key
#   %(prog)s list --tag production
#   %(prog)s rotate my_api_key
#   %(prog)s stats
#         """
#     )
#
#     parser.add_argument('--storage', default='secrets.dat',
#                         help='Storage file path (default: secrets.dat)')
#     parser.add_argument('--master-key', action='store_true',
#                         help='Prompt for master key for encryption')
#     parser.add_argument('--verbose', '-v', action='store_true',
#                         help='Enable verbose output')
#
#     subparsers = parser.add_subparsers(dest='command', help='Available commands')
#
#     # Store command
#     store_parser = subparsers.add_parser('store', help='Store a new secret')
#     store_parser.add_argument('name', help='Secret name')
#     store_parser.add_argument('--description', '-d', help='Secret description')
#     store_parser.add_argument('--tags', '-t', help='Comma-separated tags')
#
#     # Retrieve command
#     retrieve_parser = subparsers.add_parser('retrieve', help='Retrieve a secret')
#     retrieve_parser.add_argument('name', help='Secret name')
#     retrieve_parser.add_argument('--no-value', action='store_true',
#                                  help='Don\'t show the simulated secret value')
#
#     # List command
#     list_parser = subparsers.add_parser('list', help='List secrets')
#     list_parser.add_argument('--tag', help='Filter by tag')
#     list_parser.add_argument('--format', choices=['table', 'detailed'],
#                              default='table', help='Output format')
#
#     # Update command
#     update_parser = subparsers.add_parser('update', help='Update secret metadata')
#     update_parser.add_argument('name', help='Secret name')
#     update_parser.add_argument('--description', '-d', help='New description')
#     update_parser.add_argument('--tags', '-t', help='New comma-separated tags')
#
#     # Delete command
#     delete_parser = subparsers.add_parser('delete', help='Delete a secret')
#     delete_parser.add_argument('name', help='Secret name')
#     delete_parser.add_argument('--force', '-f', action='store_true',
#                                help='Skip confirmation prompt')
#
#     # Rotate command
#     rotate_parser = subparsers.add_parser('rotate', help='Rotate a secret')
#     rotate_parser.add_argument('name', help='Secret name')
#
#     # Stats command
#     stats_parser = subparsers.add_parser('stats', help='Show statistics')
#
#     # Audit command
#     audit_parser = subparsers.add_parser('audit', help='Show audit log')
#     audit_parser.add_argument('--limit', type=int, default=20,
#                               help='Number of log entries to show (default: 20)')
#
#     args = parser.parse_args()
#
#     if not args.command:
#         print_banner()
#         parser.print_help()
#         return
#
#     # Initialize CLI
#     cli = SecretManagerAdvancedCLI()
#
#     # Get master key if requested
#     master_key = None
#     if args.master_key:
#         master_key = getpass("Enter master key: ")
#
#     # Setup manager
#     if not cli.setup_manager(master_key, args.storage):
#         sys.exit(1)
#
#     # Execute command
#     try:
#         if args.command == 'store':
#             cli.store_secret(args)
#         elif args.command == 'retrieve':
#             cli.retrieve_secret(args)
#         elif args.command == 'list':
#             cli.list_secrets(args)
#         elif args.command == 'update':
#             cli.update_secret(args)
#         elif args.command == 'delete':
#             cli.delete_secret(args)
#         elif args.command == 'rotate':
#             cli.rotate_secret(args)
#         elif args.command == 'stats':
#             cli.show_stats(args)
#         elif args.command == 'audit':
#             cli.show_audit_log(args)
#         else:
#             print_error(f"Unknown command: {args.command}")
#             sys.exit(1)
#
#     except KeyboardInterrupt:
#         print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
#         sys.exit(1)
#     except Exception as e:
#         print_error(f"Unexpected error: {e}")
#         if args.verbose:
#             import traceback
#             traceback.print_exc()
#         sys.exit(1)
#
#
# if __name__ == "__main__":
#     main()