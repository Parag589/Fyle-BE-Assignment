# Import necessary modules and classes
from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

# Import schemas for data serialization/deserialization
from .schema import AssignmentSchema, AssignmentSubmitSchema, AssignmentGradeSchema, TeacherSchema

# Create a Flask Blueprint named 'principal_assignments_resources'
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

# Route to get all assignments
@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal  # Authenticate principal
def test(p):
    ''' get all the assignments '''
    # Fetch all assignments associated with the principal
    principal_assignments = Assignment.get_assignments_by_principal()
    # Serialize assignments into JSON format
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    # Return JSON response containing assignments
    return APIResponse.respond(data=principal_assignments_dump)

# Route to get the number of teachers
@principal_assignments_resources.route('/teachers')
@decorators.authenticate_principal  # Authenticate principal
def list_teachers(p):
    # Get the number of teachers
    number = TeacherSchema.get_number_of_teacher()
    # Serialize number of teachers into JSON format
    number_dump = TeacherSchema().dump(number, many=True)
    # Return JSON response containing the number of teachers
    return APIResponse.respond(data=number_dump)

# Route to grade an assignment
@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload  # Accept JSON payload
@decorators.authenticate_principal  # Authenticate principal
def grade_assignment(p, incoming_payload):
    # Deserialize incoming payload into AssignmentGradeSchema
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    # Mark the assignment with the provided grade
    graded_assignment = Assignment.mark_principal(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    # Commit changes to the database
    db.session.commit()
    # Print the graded assignment's grade
    print(graded_assignment.grade)
    # Serialize graded assignment into JSON format
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    # Return JSON response containing graded assignment
    return APIResponse.respond(data=graded_assignment_dump)
