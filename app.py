from flask import Flask, render_template, jsonify
import random
from collections import defaultdict

app = Flask(__name__)

# Your original code with slight modifications for web integration
groups = ["G1", "G2", "G3", "G4", "G5", "G6"]
days = ["Sun", "Mon", "Tue", "Wed", "Thu"]
slots_per_day = {
    "Sun": [1, 2, 3, 4, 5],
    "Mon": [1, 2, 3, 4, 5],
    "Tue": [1, 2, 3],
    "Wed": [1, 2, 3, 4, 5],
    "Thu": [1, 2, 3, 4, 5]
}

all_slots = [f"{day}-{slot}" for day in days for slot in slots_per_day[day]]

courses = {
    "Sécurité": ["lecture", "td"],
    "Méthodes formelles": ["lecture", "td"],
    "Analyse numérique": ["lecture", "td"],
    "Entrepreneuriat": ["lecture"],
    "Recherche opérationnelle 2": ["lecture", "td"],
    "Architecture Distribuée": ["lecture", "td"],
    "Réseaux 2": ["lecture", "td", "tp"],
    "IA": ["lecture", "td", "tp"]
}

teachers = {
    "Sécurité": ["T1"],
    "Méthodes formelles": ["T2"],
    "Analyse numérique": ["T3"],
    "Entrepreneuriat": ["T4"],
    "Recherche opérationnelle 2": ["T5"],
    "Architecture Distribuée": ["T6"],
    "Réseaux 2": ["T7"],
    "Réseaux 2 TP": ["T8", "T9", "T10"],
    "IA": ["T11"],
    "IA TP": ["T12", "T13", "T14"]
}

variables = []
for course, sessions in courses.items():
    if "lecture" in sessions:
        variables.append(f"{course}-lecture")
    if "td" in sessions:
        for group in groups:
            variables.append(f"{course}-td-{group}")
    if "tp" in sessions:
        for group in groups:
            variables.append(f"{course}-tp-{group}")

domains = {var: all_slots.copy() for var in variables}

def get_teachers(var):
    course, session_type, *rest = var.split("-")
    if session_type == "tp":
        return teachers.get(course + " TP", [])
    return teachers.get(course, [])

def parse_slot(slot):
    day, number = slot.split("-")
    return day, int(number)

def respect_consecutive_sessions(assignment, var, value):
    var_parts = var.split("-")
    affected_groups = []
    
    if len(var_parts) == 3:
        affected_groups = [var_parts[2]]
    elif len(var_parts) == 2 and "lecture" in var_parts[1]:
        affected_groups = groups

    for group in affected_groups:
        group_sessions = []
        for other_var, other_value in assignment.items():
            other_parts = other_var.split("-")
            if ((group in other_var) or ("lecture" in other_var)):
                group_sessions.append(other_value)
        
        group_sessions.append(value)
        
        sessions_by_day = defaultdict(list)
        for slot in group_sessions:
            day, number = parse_slot(slot)
            sessions_by_day[day].append(number)
        
        for day, slots in sessions_by_day.items():
            slots.sort()
            consecutive_count = 1
            for i in range(1, len(slots)):
                if slots[i] == slots[i-1] + 1:
                    consecutive_count += 1
                    if consecutive_count > 3:
                        return False
                else:
                    consecutive_count = 1
    return True

def verify_all_sessions_assigned(assignment):
    assigned_sessions = {group: {'td': set(), 'tp': set()} for group in groups}
    
    for var in assignment:
        parts = var.split('-')
        if len(parts) == 3:
            course, session_type, group = parts
            assigned_sessions[group][session_type].add(course)
    
    for course, sessions in courses.items():
        for group in groups:
            if 'td' in sessions and course not in assigned_sessions[group]['td']:
                return False
            if 'tp' in sessions and course not in assigned_sessions[group]['tp']:
                return False
    return True

def check_lecture_limit(assignment, var, value):
    if "lecture" not in var:
        return True
    
    day, _ = parse_slot(value)
    lecture_count = 0
    
    for assigned_var, assigned_value in assignment.items():
        if "lecture" in assigned_var:
            assigned_day, _ = parse_slot(assigned_value)
            if assigned_day == day:
                lecture_count += 1
    
    if lecture_count >= 2:
        return False
        
    return True

def get_teacher_working_days(assignment):
    teacher_days = defaultdict(set)
    for var, slot in assignment.items():
        day, _ = parse_slot(slot)
        teachers_involved = get_teachers(var)
        for teacher in teachers_involved:
            teacher_days[teacher].add(day)
    return teacher_days

def check_teacher_days(assignment, var, value):
    day, _ = parse_slot(value)
    teachers_involved = get_teachers(var)
    
    teacher_days = get_teacher_working_days(assignment)
    
    for teacher in teachers_involved:
        current_days = teacher_days.get(teacher, set())
        if day in current_days:
            continue
        if len(current_days) >= 3:
            return False
    return True

def is_consistent(assignment, var, value):
    course, session_type, *rest = var.split("-")
    group = rest[0] if rest else None
    teachers_involved = get_teachers(var)

    if "lecture" in var and not check_lecture_limit(assignment, var, value):
        return False
        
    if not check_teacher_days(assignment, var, value):
        return False

    for other_var, other_value in assignment.items():
        if value != other_value:
            continue
            
        other_course, other_session_type, *other_rest = other_var.split("-")
        other_group = other_rest[0] if other_rest else None
        
        if (group and other_group and group == other_group) or \
           (group and "lecture" in other_var) or \
           (other_group and "lecture" in var):
            return False

        other_teachers = get_teachers(other_var)
        if teachers_involved and other_teachers:
            if "tp" in var and "tp" in other_var:
                if not (set(teachers_involved) & set(other_teachers)):
                    return False
            elif set(teachers_involved) & set(other_teachers):
                return False

        if "lecture" in var and "lecture" in other_var:
            return False

    if not respect_consecutive_sessions(assignment, var, value):
        return False
        
    return True

def select_unassigned_variable(assignment):
    unassigned = [var for var in variables if var not in assignment]
    remaining_values = {}
    for var in unassigned:
        count = sum(1 for value in domains[var] if is_consistent(assignment, var, value))
        remaining_values[var] = count
    return min(remaining_values.keys(), key=lambda k: remaining_values[k]) if remaining_values else None

def order_domain_values(var, assignment):
    random.shuffle(domains[var])
    return domains[var]

def backtrack(assignment):
    if len(assignment) == len(variables):
        if verify_all_sessions_assigned(assignment):
            return assignment
        return None

    var = select_unassigned_variable(assignment)
    for value in order_domain_values(var, assignment):
        if is_consistent(assignment, var, value):
            assignment[var] = value
            result = backtrack(assignment)
            if result is not None:
                return result
            del assignment[var]
    return None

def process_solution_for_web(solution):
    if not solution:
        return None
    
    timetable = {}
    for group in groups + ["ALL"]:
        timetable[group] = {}
        for day in days:
            timetable[group][day] = {}
            for slot in slots_per_day[day]:
                timetable[group][day][slot] = []

    for var, slot in solution.items():
        day, slot_num = slot.split('-')
        parts = var.split('-')
        course = parts[0]
        session_type = parts[1]
        
        if session_type == 'lecture':
            # Lectures affect all groups
            for group in groups:
                timetable[group][day][int(slot_num)].append({
                    'course': course,
                    'type': session_type,
                    'var': var
                })
            timetable["ALL"][day][int(slot_num)].append({
                'course': course,
                'type': session_type,
                'var': var
            })
        else:
            # TD/TP affect specific group
            group = parts[2]
            timetable[group][day][int(slot_num)].append({
                'course': course,
                'type': session_type,
                'var': var
            })
            # Also add to ALL view
            timetable["ALL"][day][int(slot_num)].append({
                'course': f"{course} ({group})",  # Include group in the course name
                'type': session_type,
                'var': var
            })
    
    # Generate course colors
    course_colors = {}
    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5'
    ]
    
    for i, course in enumerate(courses.keys()):
        course_colors[course] = colors[i % len(colors)]
    
    return {
        'timetable': timetable,
        'course_colors': course_colors,
        'courses': list(courses.keys()),
        'days': days,
        'slots_per_day': slots_per_day,
        'groups': groups
    }
# Cache the solution to avoid recomputing on every request
cached_solution = None
from flask_cors import CORS
CORS(app)  # Enable CORS for all routes
@app.route('/')
def index():
    return render_template('timetable.html')

@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    global cached_solution
    cached_solution = None
    return jsonify({'status': 'cache_cleared'})

@app.route('/generate_timetable')
def generate_timetable():
    global cached_solution
    
    if not cached_solution:
        solution = backtrack({})
        if not solution:
            return jsonify({'error': 'No solution found'}), 400
        
        cached_solution = process_solution_for_web(solution)
    
    return jsonify(cached_solution)

if __name__ == '__main__':
    app.run(debug=True)