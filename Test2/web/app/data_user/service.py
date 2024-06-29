from flask import Blueprint,render_template, request, redirect, url_for, flash, session, jsonify, current_app as app
from pypbc import Parameters, Element,Pairing, G1,G2,Zr
import requests
from cryptography.fernet import Fernet
from collections import defaultdict
from ..models import User
from .. import db
import random
views = Blueprint('views',__name__)



def get_keywords_list(keywords):
    cleaned_keywords = keywords.strip("{}")
    elements = cleaned_keywords.split(",")
    elements = [elem.strip() for elem in elements]
    return elements

def trapdoor(params,  query_word):
    # Use tk to generate the trapdoor
    # Td = []
    # for word in query_words:
    Td = Element(params["e"], G1, value = params['H1'](query_word))
    return Td

