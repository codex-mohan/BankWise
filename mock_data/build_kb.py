import json
import os
import glob
import markdown2
import pdfkit
from datetime import datetime

# --- Helper Functions ---


def get_status_color(status):
    """Returns a color based on status for HTML formatting in Markdown."""
    if not status:
        return "black"
    status = status.upper()
    if status in ["AVAILABLE", "ACTIVE", "VERIFIED"]:
        return "green"
    if status in ["BUSY", "ON BREAK", "IN TRAINING", "UNDER_REVIEW"]:
        return "orange"
    if status in ["OFF DUTY", "INACTIVE", "FROZEN", "PENDING"]:
        return "red"
    return "black"


# --- Formatting Functions (JSON to Markdown) ---


def generate_agents_md(data):
    """Generates comprehensive Markdown content for the agents list."""
    md_lines = ["## 👨‍💼 BankWise Agent Directory\n"]
    for agent in data:
        status_color = get_status_color(agent.get("current_status"))
        md_lines.append(
            f"### {agent.get('full_name', 'N/A')} ({agent.get('agent_id', 'N/A')})"
        )
        md_lines.append(
            f"* **Status**: <font color=\"{status_color}\">{agent.get('current_status', 'N/A')}</font>"
        )
        md_lines.append(
            f"* **Contact**: {agent.get('email', 'N/A')} | {agent.get('phone', 'N/A')}"
        )
        md_lines.append(f"* **Department**: {agent.get('department', 'N/A')}")
        md_lines.append(f"* **Specialization**: {agent.get('specialization', 'N/A')}")
        md_lines.append(
            f"* **Experience**: {agent.get('years_experience', 'N/A')} years | **Escalation Level**: {agent.get('escalation_level', 'N/A')}"
        )
        md_lines.append(
            f"* **Performance**: {agent.get('performance_rating', 0.0)}★ | **Customer Satisfaction**: {agent.get('customer_satisfaction_rate', 0.0)}%"
        )
        md_lines.append(
            f"* **Schedule**: {agent.get('working_days', 'N/A')} ({agent.get('shift_start', '')} - {agent.get('shift_end', '')})"
        )
        md_lines.append(
            f"* **Languages**: {', '.join(agent.get('languages_spoken', []))}"
        )
        md_lines.append(f"* **Skills**: {', '.join(agent.get('skills', []))}")
        md_lines.append(
            f"* **Certifications**: {', '.join(agent.get('certifications', []))}\n"
        )
    return "\n".join(md_lines)


def generate_accounts_md(data):
    """Generates comprehensive and RAG-optimized Markdown for the accounts list."""
    md_lines = ["## 🏦 Customer Account Details\n"]
    for acc in data:
        acc_status_color = get_status_color(acc.get("account_status"))
        kyc_status_color = get_status_color(acc.get("kyc_status"))

        md_lines.append(f"### {acc.get('customer_name', 'N/A')}")
        md_lines.append(f"* **Account Number**: `{acc.get('account_number', 'N/A')}`")
        md_lines.append(f"* **Account Type**: {acc.get('account_type', 'N/A')}")
        md_lines.append(
            f"* **Balance**: ₹{acc.get('balance', 0):,.2f} ({acc.get('currency', 'N/A')})"
        )
        md_lines.append(
            f"* **Account Status**: <font color=\"{acc_status_color}\">{acc.get('account_status', 'N/A')}</font>"
        )
        md_lines.append(
            f"* **KYC Status**: <font color=\"{kyc_status_color}\">{acc.get('kyc_status', 'N/A')} (Level: {acc.get('kyc_level', 'N/A')})</font>"
        )
        md_lines.append(f"* **Customer ID**: {acc.get('customer_id', 'N/A')}")
        md_lines.append(
            f"* **Branch**: {acc.get('branch_code', 'N/A')} / {acc.get('ifsc_code', 'N/A')}"
        )
        md_lines.append(
            f"* **Linked Cards**: {', '.join(acc.get('linked_cards', ['None']))}"
        )
        md_lines.append(
            f"* **Registered Mobile Numbers**: {', '.join(acc.get('mobile_numbers', ['None']))}"
        )

        last_updated_str = acc.get("last_updated", "")
        if last_updated_str:
            last_updated_dt = datetime.fromisoformat(last_updated_str)
            md_lines.append(
                f"* **Last Updated**: {last_updated_dt.strftime('%d-%b-%Y %I:%M %p')}\n"
            )
        else:
            md_lines.append("* **Last Updated**: N/A\n")

    return "\n".join(md_lines)


def generate_fd_rates_md(data):
    """Generates a comprehensive Markdown table for FD rates."""
    md_lines = [
        "## 📈 Fixed Deposit Interest Rates\n",
        "| Tenure (Days) | Customer Type | Rate (%) | Min Amount (INR) | Max Amount (INR) | Special Features |",
        "| :------------ | :------------ | :------- | :--------------- | :--------------- | :----------------- |",
    ]
    last_update_date = None
    for rate_info in data:
        md_lines.append(
            f"| {rate_info.get('tenure', 'N/A'):<13} "
            f"| {rate_info.get('customer_type', 'N/A'):<14} "
            f"| {rate_info.get('rate', 0.0):<8.2f} "
            f"| {rate_info.get('min_amount', 0):<16,} "
            f"| {rate_info.get('max_amount', 0):<16,} "
            f"| {rate_info.get('special_features', 'N/A'):<18} |"
        )
        if rate_info.get("last_updated"):
            current_date = datetime.fromisoformat(rate_info.get("last_updated"))
            if not last_update_date or current_date > last_update_date:
                last_update_date = current_date

    if last_update_date:
        md_lines.append(
            f"\n_Rates last updated on: {last_update_date.strftime('%d-%b-%Y')}_"
        )

    return "\n".join(md_lines)


# --- PDF Conversion Function ---


def convert_md_to_pdf(md_filepath, pdf_filepath):
    """Converts a single Markdown file to a PDF with styling."""
    try:
        with open(md_filepath, "r", encoding="utf-8") as f:
            md_content = f.read()

        html_content = markdown2.markdown(
            md_content, extras=["tables", "fenced-code-blocks", "cuddled-lists"]
        )

        html_with_style = f"""
        <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; }}
                    h2 {{ color: #1a237e; border-bottom: 2px solid #3f51b5; padding-bottom: 8px; }}
                    h3 {{ color: #3f51b5; }}
                    table {{ border-collapse: collapse; width: 100%; margin-top: 1em; }}
                    th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
                    th {{ background-color: #f2f5fc; font-weight: bold; }}
                    code {{ background-color: #e8eaf6; color: #3f51b5; padding: 3px 6px; border-radius: 4px; font-family: "Courier New", Courier, monospace; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    li {{ margin-bottom: 0.5em; }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
        </html>
        """
        pdfkit.from_string(html_with_style, pdf_filepath)
        print(f"📄 Successfully created PDF: '{os.path.basename(pdf_filepath)}'")
    except FileNotFoundError:
        print(
            "❌ Error: wkhtmltopdf not found. Please ensure it's installed and in your system's PATH."
        )
        print("Download from: https://wkhtmltopdf.org/downloads.html")
    except Exception as e:
        print(
            f"❌ An unexpected error occurred during PDF conversion for '{os.path.basename(md_filepath)}': {e}"
        )


# --- Main Processing Logic ---

FORMATTER_DISPATCHER = {
    "agents": generate_agents_md,
    "accounts": generate_accounts_md,
    "fd_rates": generate_fd_rates_md,
}


def process_json_files(input_dir, md_output_dir, pdf_output_dir):
    """Finds JSON files, converts them to Markdown, and then to PDF."""
    print(f"Searching for JSON files in: '{input_dir}'")
    os.makedirs(md_output_dir, exist_ok=True)
    os.makedirs(pdf_output_dir, exist_ok=True)

    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    if not json_files:
        print("No JSON files found to process.")
        return

    for json_filepath in json_files:
        filename = os.path.basename(json_filepath)
        base_name = os.path.splitext(filename)[0]

        formatter = FORMATTER_DISPATCHER.get(base_name)
        if not formatter:
            print(f"⚠️  Skipping '{filename}': No formatter found.")
            continue

        try:
            with open(json_filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            markdown_content = formatter(data)
            md_filename = f"{base_name}.md"
            md_filepath = os.path.join(md_output_dir, md_filename)
            with open(md_filepath, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            print(f"✅ Successfully converted '{filename}' to '{md_filename}'")

            pdf_filename = f"{base_name}.pdf"
            pdf_filepath = os.path.join(pdf_output_dir, pdf_filename)
            convert_md_to_pdf(md_filepath, pdf_filepath)

        except json.JSONDecodeError:
            print(f"❌ Error: Could not decode JSON in '{filename}'.")
        except Exception as e:
            print(f"❌ An unexpected error occurred processing '{filename}': {e}")


if __name__ == "__main__":
    INPUT_DIR = "json_data"
    MD_OUTPUT_DIR = "markdown_output"
    PDF_OUTPUT_DIR = "pdf_output"

    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        print(f"Created dummy input directory '{INPUT_DIR}'.")
        print("Please place your JSON files there and run again.")

    process_json_files(INPUT_DIR, MD_OUTPUT_DIR, PDF_OUTPUT_DIR)
