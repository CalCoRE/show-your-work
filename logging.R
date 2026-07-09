library(tidyverse)
library(glue)

# notebook <- "0 - IntroR"


log_cell_run <- function(code_expr){
  start_datetime <- lubridate::now()
  start_date <- format(start_datetime, "%Y_%m_%d")
  timestamp_str <- format(start_datetime, "%Y%m%d_%H%M%OS3")
  status <- "Success"

  code_text <- paste(
    deparse(
      substitute(
        code_expr
      )
    ),
    collapse = "\n"
  )

  # Evaluate code safely
  result <- tryCatch({
    eval(
      substitute(
        code_expr
      ),
      envir = parent.frame()
    )
  },
  error = function(e) {
    status <<- "Error"
    message("Execution Error: ", e$message)
  })

  log_entry <- tibble::tibble(
    Timestamp = format(start_datetime, "%Y-%m-%d %H:%M:%S"),
    Status    = status,
    Code      = code_text
  )

  # Write each run to its own temp file to avoid overlap
  tmp_dir  <- here::here(glue::glue("meta_{notebook}_tmp"))
  dir.create(tmp_dir, showWarnings = FALSE)
  tmp_path <- file.path(tmp_dir, glue::glue("{timestamp_str}.csv"))

  write.table(
    log_entry,
    tmp_path,
    sep       = ",",
    row.names = FALSE,
    col.names = TRUE,
    quote     = TRUE
  )

  return(invisible(result))
}

# Concatenate all temp CSVs into a single daily log file
compile_log <- function() {
  start_date <- format(lubridate::now(), "%Y_%m_%d")
  tmp_dir    <- here::here(glue::glue("meta_{notebook}_tmp"))
  tmp_files  <- list.files(tmp_dir, pattern = "\\.csv$", full.names = TRUE)

  if (length(tmp_files) == 0) {
    message("No log entries to compile.")
    return(invisible(NULL))
  }

  combined <- purrr::map(tmp_files, readr::read_csv, show_col_types = FALSE) |>
    dplyr::bind_rows()

  out_path <- here::here(glue::glue("meta_{notebook}_{start_date}.csv"))
  readr::write_csv(combined, out_path)

  message(glue::glue("Compiled {nrow(combined)} entries to {out_path}"))
  return(invisible(combined))
}