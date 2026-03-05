"""
Flask web application for the Nagios Configuration Generator.

Provides a web UI where users can input host/service/contact details
via a form and download generated Nagios .cfg files as a ZIP archive.
"""

import json
import traceback

from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import io

from src.main.models import NagiosConfig, Host, Service, Contact, ContactGroup
from src.main.generator import NagiosGenerator

app = Flask(
    __name__,
    template_folder="../../templates/web",
    static_folder="../../static",
)
app.secret_key = "nagiosgen-secret-key-change-in-production"


@app.route("/")
def index():
    """Render the main configuration form."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """Process form data and return generated configs."""
    try:
        # Parse hosts from form
        hosts = []
        host_names = request.form.getlist("host_name[]")
        host_aliases = request.form.getlist("host_alias[]")
        host_addresses = request.form.getlist("host_address[]")
        host_groups_list = request.form.getlist("host_contact_groups[]")

        for i in range(len(host_names)):
            if host_names[i].strip():
                hosts.append(Host(
                    host_name=host_names[i].strip(),
                    alias=host_aliases[i].strip() if i < len(host_aliases) else host_names[i].strip(),
                    address=host_addresses[i].strip() if i < len(host_addresses) else "127.0.0.1",
                    contact_groups=(
                        host_groups_list[i].strip()
                        if i < len(host_groups_list) and host_groups_list[i].strip()
                        else "admins"
                    ),
                ))

        # Parse services from form
        services = []
        svc_hosts = request.form.getlist("svc_host_name[]")
        svc_descs = request.form.getlist("svc_description[]")
        svc_cmds = request.form.getlist("svc_check_command[]")

        for i in range(len(svc_hosts)):
            if svc_hosts[i].strip():
                services.append(Service(
                    host_name=svc_hosts[i].strip(),
                    service_description=svc_descs[i].strip() if i < len(svc_descs) else "Service Check",
                    check_command=svc_cmds[i].strip() if i < len(svc_cmds) else "check_ping",
                ))

        # Parse contacts from form
        contacts = []
        contact_names = request.form.getlist("contact_name[]")
        contact_aliases = request.form.getlist("contact_alias[]")
        contact_emails = request.form.getlist("contact_email[]")

        for i in range(len(contact_names)):
            if contact_names[i].strip():
                contacts.append(Contact(
                    contact_name=contact_names[i].strip(),
                    alias=contact_aliases[i].strip() if i < len(contact_aliases) else contact_names[i].strip(),
                    email=contact_emails[i].strip() if i < len(contact_emails) else "admin@example.com",
                ))

        # Parse contact groups
        contact_groups = []
        cg_names = request.form.getlist("cg_name[]")
        cg_aliases = request.form.getlist("cg_alias[]")
        cg_members = request.form.getlist("cg_members[]")

        for i in range(len(cg_names)):
            if cg_names[i].strip():
                contact_groups.append(ContactGroup(
                    contactgroup_name=cg_names[i].strip(),
                    alias=cg_aliases[i].strip() if i < len(cg_aliases) else cg_names[i].strip(),
                    members=cg_members[i].strip() if i < len(cg_members) else "",
                ))

        if not hosts and not services and not contacts:
            flash("Please add at least one host, service, or contact.", "error")
            return redirect(url_for("index"))

        # Build config and generate
        config = NagiosConfig(
            hosts=hosts,
            services=services,
            contacts=contacts,
            contact_groups=contact_groups,
        )

        generator = NagiosGenerator()
        rendered = generator.generate(config)

        return render_template("result.html", configs=rendered, config=config)

    except Exception as e:
        traceback.print_exc()
        flash(f"Error generating configuration: {str(e)}", "error")
        return redirect(url_for("index"))


@app.route("/download", methods=["POST"])
def download():
    """Generate and download configs as a ZIP file."""
    try:
        configs_json = request.form.get("configs_json", "{}")
        configs_data = json.loads(configs_json)

        config = NagiosConfig.from_dict(configs_data)
        generator = NagiosGenerator()
        zip_bytes = generator.generate_zip(config)

        return send_file(
            io.BytesIO(zip_bytes),
            mimetype="application/zip",
            as_attachment=True,
            download_name="nagios_configs.zip",
        )
    except Exception as e:
        traceback.print_exc()
        flash(f"Error creating download: {str(e)}", "error")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
