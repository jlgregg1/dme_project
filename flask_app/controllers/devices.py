from flask import Flask, flash, session, render_template, redirect, request
from flask_app import app
from flask_app.models import user, device
from flask_app.controllers import users