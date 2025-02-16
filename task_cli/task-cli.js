#!/usr/bin/env node
const fs = require('fs');

function loadTasks() {
  try {
    const data = fs.readFileSync('tasks.json', 'utf8');
    return JSON.parse(data);
  } catch (error) {
    return [];
  }
}

function saveTasks(tasks) {
  fs.writeFileSync('tasks.json', JSON.stringify(tasks, null, 2));
}

function addTask() {
  const description = process.argv[3];
  if (!description) {
    console.error('Error: Missing task description.');
    process.exit(1);
  }

  const tasks = loadTasks();
  const newId = tasks.length > 0 ? Math.max(...tasks.map(t => t.id)) + 1 : 1;
  const now = new Date().toISOString();
  
  tasks.push({
    id: newId,
    description,
    status: 'todo',
    createdAt: now,
    updatedAt: now
  });
  
  saveTasks(tasks);
  console.log(`Task added successfully (ID: ${newId})`);
}

function updateTask() {
  const id = parseInt(process.argv[3]);
  const newDescription = process.argv[4];

  if (isNaN(id) || !newDescription) {
    console.error('Error: Invalid ID or missing description.');
    process.exit(1);
  }

  const tasks = loadTasks();
  const task = tasks.find(t => t.id === id);

  if (!task) {
    console.error(`Error: Task with ID ${id} not found.`);
    process.exit(1);
  }

  task.description = newDescription;
  task.updatedAt = new Date().toISOString();
  saveTasks(tasks);
  console.log(`Task ${id} updated successfully.`);
}

function deleteTask() {
  const id = parseInt(process.argv[3]);
  if (isNaN(id)) {
    console.error('Error: Invalid ID.');
    process.exit(1);
  }

  const tasks = loadTasks();
  const initialLength = tasks.length;
  const filteredTasks = tasks.filter(t => t.id !== id);

  if (filteredTasks.length === initialLength) {
    console.error(`Error: Task with ID ${id} not found.`);
    process.exit(1);
  }

  saveTasks(filteredTasks);
  console.log(`Task ${id} deleted successfully.`);
}

function markTask(status) {
  const id = parseInt(process.argv[3]);
  if (isNaN(id)) {
    console.error('Error: Invalid ID.');
    process.exit(1);
  }

  const tasks = loadTasks();
  const task = tasks.find(t => t.id === id);

  if (!task) {
    console.error(`Error: Task with ID ${id} not found.`);
    process.exit(1);
  }

  task.status = status;
  task.updatedAt = new Date().toISOString();
  saveTasks(tasks);
  console.log(`Task ${id} marked as ${status}.`);
}

function listTasks() {
  const statusFilter = process.argv[3];
  const validStatuses = ['todo', 'in-progress', 'done'];
  
  if (statusFilter && !validStatuses.includes(statusFilter)) {
    console.error('Error: Invalid status. Valid statuses: todo, in-progress, done');
    process.exit(1);
  }

  const tasks = loadTasks();
  const filteredTasks = statusFilter 
    ? tasks.filter(t => t.status === statusFilter)
    : tasks;

  if (filteredTasks.length === 0) {
    console.log('No tasks found.');
    return;
  }

  console.log(`Tasks (${statusFilter || 'all'}):`);
  filteredTasks.forEach(task => {
    console.log(`ID: ${task.id}`);
    console.log(`Description: ${task.description}`);
    console.log(`Status: ${task.status}`);
    console.log(`Created: ${task.createdAt}`);
    console.log(`Updated: ${task.updatedAt}`);
    console.log('---');
  });
}

const action = process.argv[2];

switch (action) {
  case 'add':
    addTask();
    break;
  case 'update':
    updateTask();
    break;
  case 'delete':
    deleteTask();
    break;
  case 'mark-in-progress':
    markTask('in-progress');
    break;
  case 'mark-done':
    markTask('done');
    break;
  case 'list':
    listTasks();
    break;
  default:
    console.error('Error: Invalid action. Available actions:');
    console.error('add, update, delete, mark-in-progress, mark-done, list');
    process.exit(1);
}