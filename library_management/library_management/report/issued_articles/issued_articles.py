import frappe


def execute(filters=None):
    filters = filters or {}
    return get_columns(), get_data(filters)


def get_columns():
    return [
        "Article:Link/Article:150",
        "Author::150",
        "Category::120",
        "Member:Link/Library Member:150",
    ]


def get_data(filters):
    category_condition = ""
    if filters.get("category"):
        category_condition = "AND a.category = %(category)s"

    return frappe.db.sql(
        f"""
        SELECT a.name, a.author, a.category, t.library_member
        FROM `tabArticle` a
        LEFT JOIN `tabLibrary Transaction` t
            ON t.name = (
                SELECT t2.name
                FROM `tabLibrary Transaction` t2
                WHERE t2.article = a.name
                  AND t2.docstatus = 1
                  AND t2.type = 'Issue'
                ORDER BY t2.date DESC, t2.creation DESC
                LIMIT 1
            )
        WHERE a.status = 'Issued' {category_condition}
        """,
        filters,
    )