from flask import Blueprint
import logging

logger = logging.getLogger(__name__)

api = Blueprint('api', __name__)
logger.info("API blueprint created")

from . import match
logger.info("API routes imported")