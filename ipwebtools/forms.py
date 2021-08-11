# Copyright (c) 2021, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Application forms."""
from starlette_wtf import StarletteForm
from wtforms import TextAreaField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class CidrMergeForm(StarletteForm):
    """Form for CIDR Merge Page."""

    networks = TextAreaField("IP Networks", validators=[DataRequired()])
    excluded = TextAreaField("Excluded Networks")
    submit = SubmitField("Submit")


class CidrSplitForm(StarletteForm):
    """Form for CIDR Split Page."""

    network = StringField("IP CIDR", validators=[DataRequired()])
    mask = IntegerField("Split Prefix Length", validators=[DataRequired(), NumberRange(min=1, max=128)])
    submit = SubmitField("Submit")


class CidrInfoForm(StarletteForm):
    """Form for CIDR Info Page."""

    network = StringField("IP CIDR", validators=[DataRequired()])
    submit = SubmitField("Submit")
