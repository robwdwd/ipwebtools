# Copyright (c) 2024, Rob Woodward. All rights reserved.
#
# This file is part of IP Web Tools and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Application forms."""
from starlette_wtf import StarletteForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange


class CidrMergeForm(StarletteForm):
    """Form for IP Prefix Merge Page."""

    networks = TextAreaField("IP Networks", validators=[DataRequired()])
    excluded = TextAreaField("Excluded Networks")
    submit = SubmitField("Submit")


class CidrSplitForm(StarletteForm):
    """Form for IP Prefix Split Page."""

    network = StringField("IP Prefix", validators=[DataRequired()])
    mask = IntegerField("Split Prefix Length", validators=[DataRequired(), NumberRange(min=1, max=128)])
    submit = SubmitField("Submit")


class PrefixInfoForm(StarletteForm):
    """Form for IP Prefix Info Page."""

    network = StringField("IP Prefix", validators=[DataRequired()])
    submit = SubmitField("Submit")


class IPInfoForm(StarletteForm):
    """Form for IP Info Page."""

    ipaddress = StringField("IP Address", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ASNInfoForm(StarletteForm):
    """Form for ASN Info Page."""

    asn = IntegerField("ASN", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Submit")
