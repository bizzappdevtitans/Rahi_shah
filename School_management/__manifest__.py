{
    "name": "School management ",
    "version": "1.0",
    "category": "Management/Management",
    "summary": "School Management",
    "author": "BizzAppDev",
    "description": """
This module contains all the common features of School Management.
    """,
    "depends": ["mail","sale"],
    "data": [
        "Data/seq.xml",
        "Data/server_action.xml",
        "Data/cron.xml",
        "security/ir.model.access.csv",
        "security/school_security.xml",
        "wizard/demo_wizard_view.xml",
        "wizard/student_grade_view_wizard.xml",
        "wizard/create_student_wizard_view.xml",
        "views/inherit_desc.xml",
        "views/school_student_view.xml",
        "views/school_menu.xml",
        "views/school_teacher_view.xml",
        "views/school_submit_assignment_view.xml",
        
    ],
    "license": "LGPL-3",
}
