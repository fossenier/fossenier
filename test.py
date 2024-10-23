from graphviz import Digraph

# Initialize a directed graph
dot = Digraph(comment="CMPT Courses Dependency Graph", format="png")

# Define courses
courses = {
    "CMPT 100": {},
    "CMPT 105": {},
    "CMPT 111": {},
    "CMPT 113": {},
    "CMPT 116": {},
    "CMPT 140.3": {"CMPT 100"},
    "CMPT 141.3": {"CMPT 140.3", "CMPT 100", "BINF 151.3", "Computer Science 30"},
    "CMPT 142.3": {
        "Mathematics B30",
        "Foundations of Mathematics 30",
        "Pre-Calculus 30",
    },
    "CMPT 145.3": {"CMPT 141.3", "CMPT 142.3", "CMPT 111.3"},
    "CMPT 146.3": {"CMPT 141.3", "CMPT 142.3"},
    "CMPT 214.3": {"CMPT 145.3", "CMPT 146.3", "CMPT 115.3", "CMPT 117.3"},
    "CMPT 215.3": {"CMPT 214.3", "Various Math Courses"},
    "CMPT 260.3": {
        "CMPT 145.3",
        "CMPT 146.3",
        "CMPT 115.3",
        "CMPT 117.3",
        "MATH110.3",
        "MATH 133.4",
        "MATH 163.3",
        "MATH 176.3",
    },
    "CMPT 263.3": {"CMPT 260.3", "MATH 163.3", "CMPT 145.3"},
    "CMPT 270.3": {
        "CMPT 145.3",
        "CMPT 146.3",
        "CMPT 115.3",
        "CMPT 117.3",
        "Various Math Courses",
    },
    "CMPT 280.3": {"CMPT 270.3"},
    "CMPT 281.3": {"CMPT 141.3", "CMPT 111.3"},
    "BINF 151.3": {},  # Assuming BINF 151.3 is a course similar to CMPT courses
    "Computer Science 30": {},  # Assuming this is a prerequisite course
    "Mathematics B30": {},
    "Foundations of Mathematics 30": {},
    "Pre-Calculus 30": {},
    "Various Math Courses": {},  # Placeholder for multiple math courses
    "CMPT 115.3": {},
    "CMPT 117.3": {},
}

# Add nodes to the graph
for course in courses:
    dot.node(course, course)

# Define edges based on prerequisites
prerequisites = {
    "CMPT 140.3": ["CMPT 100"],
    "CMPT 141.3": ["CMPT 140.3", "CMPT 100", "BINF 151.3", "Computer Science 30"],
    "CMPT 142.3": [
        "Mathematics B30",
        "Foundations of Mathematics 30",
        "Pre-Calculus 30",
    ],
    "CMPT 145.3": ["CMPT 141.3", "CMPT 142.3", "CMPT 111.3"],
    "CMPT 146.3": ["CMPT 141.3", "CMPT 142.3"],
    "CMPT 214.3": ["CMPT 145.3", "CMPT 146.3", "CMPT 115.3", "CMPT 117.3"],
    "CMPT 215.3": ["CMPT 214.3", "Various Math Courses"],
    "CMPT 260.3": [
        "CMPT 145.3",
        "CMPT 146.3",
        "CMPT 115.3",
        "CMPT 117.3",
        "MATH110.3",
        "MATH 133.4",
        "MATH 163.3",
        "MATH 176.3",
    ],
    "CMPT 263.3": ["CMPT 260.3", "MATH 163.3", "CMPT 145.3"],
    "CMPT 270.3": [
        "CMPT 145.3",
        "CMPT 146.3",
        "CMPT 115.3",
        "CMPT 117.3",
        "Various Math Courses",
    ],
    "CMPT 280.3": ["CMPT 270.3"],
    "CMPT 281.3": ["CMPT 141.3", "CMPT 111.3"],
}

# Add edges to the graph
for course, prereqs in prerequisites.items():
    for prereq in prereqs:
        if prereq in courses:
            dot.edge(prereq, course)
        else:
            # If the prerequisite is not a CMPT course, add it as a separate node
            dot.node(prereq, prereq, shape="box", style="dashed")
            dot.edge(prereq, course)

# Render the graph to a file
dot.render("cmpt_courses_dependency_graph", view=True)
