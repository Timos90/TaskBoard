/**
 * TaskColumn - Kanban board column component
 * 
 * Displays a column of tasks for a specific status (To Do, In Progress, Done).
 * Shows the status label, task count, and renders all tasks in that status.
 */

import TaskCard from "./TaskCard.jsx";

// Maps status values to user-friendly labels
const STATUS_LABELS = {
    pending: "To Do",
    started: "In Progress",
    completed: "Done"
}

/**
 * @param {string} status - Task status (pending/started/completed)
 * @param {Array} tasks - Array of tasks to display in this column
 * @param {Function} onEdit - Callback for editing tasks
 * @param {Function} onDelete - Callback for deleting tasks
 */
function TaskColumn({status, tasks, onEdit, onDelete}) {
    return <div className={"kanban-column"}>
        <div className={`kanban-column-header kanban-column-header-${status}`}>
            <h3 className={"kanban-column-title"}>{STATUS_LABELS[status]}</h3>
            <span className={"kanban-column-count"}>{tasks.length}</span>
        </div>
        <div className={"kanban-column-body"}>
            {tasks.map(task =>
                (<TaskCard
                    key={task.id}
                    task={task}
                    onEdit={onEdit}
                    onDelete={onDelete}
                />))}
        </div>
    </div>
}

export default TaskColumn