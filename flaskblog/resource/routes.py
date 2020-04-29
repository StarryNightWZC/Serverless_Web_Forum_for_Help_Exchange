from flask import (render_template, url_for, flash, current_app,redirect, request, abort, Blueprint)

resource = Blueprint('resource', __name__)

@resource.route("/resourceguide/medical")
def medical():
    return render_template('resource_guide/medical.html', title='Medical/Mental Health')

@resource.route("/resourceguide/food")
def food():
    return render_template('resource_guide/food.html', title='Food/Other Necessities')

@resource.route("/resourceguide/utility")
def utility():
    return render_template('resource_guide/utility.html', title='Utilities')

@resource.route("/resourceguide/house")
def house():
    return render_template('resource_guide/house.html', title='Housing/Shelter')

@resource.route("/resourceguide/child")
def child():
    return render_template('resource_guide/child.html', title='Youth/Child Care')

@resource.route("/resourceguide/senior")
def senior():
    return render_template('resource_guide/senior.html', title='Seniors')

@resource.route("/resourceguide/other")
def other():
    return render_template('resource_guide/other.html', title='Other Support Services')