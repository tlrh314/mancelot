#!/bin/bash
set -e

# usage: file_env VAR [DEFAULT]
#    ie: file_env 'XYZ_DB_PASSWORD' 'example'
# (will allow for "$XYZ_DB_PASSWORD_FILE" to fill in the value of
#  "$XYZ_DB_PASSWORD" from a file, especially for Docker's secrets feature)
file_env() {
	local var="$1"
	local fileVar="${var}_FILE"
	local def="${2:-}"
	if [ "${!var:-}" ] && [ "${!fileVar:-}" ]; then
		echo >&2 "error: both $var and $fileVar are set (but are exclusive)"
		exit 1
	fi
	local val="$def"
	if [ "${!var:-}" ]; then
		val="${!var}"
	elif [ "${!fileVar:-}" ]; then
		val="$(< "${!fileVar}")"
	fi
	export "$var"="$val"
	unset "$fileVar"
}

if [ "${1:0:1}" = '-' ]; then
	set -- postgres "$@"
fi

# allow the container to be started with `--user`
if [ "$1" = 'postgres' ] && [ "$(id -u)" = '0' ]; then
	mkdir -p "$PGDATA"
	chown -R postgres "$PGDATA"
	chmod 700 "$PGDATA"

	mkdir -p /var/run/postgresql
	chown -R postgres /var/run/postgresql
	chmod g+s /var/run/postgresql

	# Create the transaction log directory before initdb is run (below) so the directory is owned by the correct user
	if [ "$POSTGRES_INITDB_XLOGDIR" ]; then
		mkdir -p "$POSTGRES_INITDB_XLOGDIR"
		chown -R postgres "$POSTGRES_INITDB_XLOGDIR"
		chmod 700 "$POSTGRES_INITDB_XLOGDIR"
	fi

	mkdir -p /var/lib/postgresql
	touch /var/lib/postgresql/.pgpass
	{ echo; echo "${POSTGRES_REPLICATION_MASTER_HOST}:${POSTGRES_REPLICATION_MASTER_PORT}:*:${POSTGRES_REPLICATION_USER}:${POSTGRES_REPLICATION_PASSWORD}"; } | tee -a "/var/lib/postgresql/.pgpass" > /dev/null
	chmod 0600 /var/lib/postgresql/.pgpass
	chown -R postgres: /var/lib/postgresql

	exec su-exec postgres "$BASH_SOURCE" "$@"
fi

if [ "$1" = 'postgres' ]; then

	mkdir -p "$PGDATA"
	chown -R "$(id -u)" "$PGDATA" 2>/dev/null || :
	chmod 700 "$PGDATA" 2>/dev/null || :

	# look specifically for PG_VERSION, as it is expected in the DB dir to see if we need to initialize the db or
	# if the container just rebooted
	if [ ! -s "$PGDATA/PG_VERSION" ]; then

		file_env 'POSTGRES_INITDB_ARGS'
		if [ "$POSTGRES_INITDB_XLOGDIR" ]; then
			export POSTGRES_INITDB_ARGS="$POSTGRES_INITDB_ARGS --xlogdir $POSTGRES_INITDB_XLOGDIR"
		fi

		if [ "$POSTGRES_REPLICATION_MODE" = 'master' ]; then
			# User selected master replication mode
			echo "Master Mode Selected";

			eval "initdb --username=postgres $POSTGRES_INITDB_ARGS"

			{ echo; echo "wal_level = hot_standby"; } | tee -a "$PGDATA/postgresql.conf" > /dev/null
			{ echo; echo "archive_mode = on"; } | tee -a "$PGDATA/postgresql.conf" > /dev/null
			{ echo; echo "archive_command = 'cd .'"; } | tee -a "$PGDATA/postgresql.conf" > /dev/null
			{ echo; echo "max_wal_senders = 3"; } | tee -a "$PGDATA/postgresql.conf" > /dev/null
			{ echo; echo "wal_keep_segments = 10"; } | tee -a "$PGDATA/postgresql.conf" > /dev/null
			{ echo; echo "hot_standby = on"; } | tee -a "$PGDATA/postgresql.conf" > /dev/null

		elif [ "$POSTGRES_REPLICATION_MODE" = 'slave' ]; then
			# User selected slave replication mode
			echo "Slave Mode Selected";

			until pg_basebackup -h ${POSTGRES_REPLICATION_MASTER_HOST} -p ${POSTGRES_REPLICATION_MASTER_PORT} -D ${PGDATA} -U ${POSTGRES_REPLICATION_USER} -vP
			do
				echo "Waiting for master..."
				sleep 3s
			done

			{ echo; echo "wal_level = hot_standby"; } | tee -a "$PGDATA/postgresql.conf" > /dev/null
			{ echo; echo "archive_mode = on"; } | tee -a "$PGDATA/postgresql.conf" > /dev/null
			{ echo; echo "archive_command = 'cd .'"; } | tee -a "$PGDATA/postgresql.conf" > /dev/null
			{ echo; echo "max_wal_senders = 3"; } | tee -a "$PGDATA/postgresql.conf" > /dev/null
			{ echo; echo "wal_keep_segments = 10"; } | tee -a "$PGDATA/postgresql.conf" > /dev/null
			{ echo; echo "hot_standby = on"; } | tee -a "$PGDATA/postgresql.conf" > /dev/null

			{ echo; echo "standby_mode = 'on'"; } | tee -a "$PGDATA/recovery.conf" > /dev/null
			{ echo; echo "primary_conninfo = 'host=$POSTGRES_REPLICATION_MASTER_HOST port=$POSTGRES_REPLICATION_MASTER_PORT user=$POSTGRES_REPLICATION_USER password=$POSTGRES_REPLICATION_PASSWORD'"; } | tee -a "$PGDATA/recovery.conf" > /dev/null
			{ echo; echo "trigger_file = '/tmp/postgresql.trigger.5432'"; } | tee -a "$PGDATA/recovery.conf" > /dev/null


		else
			# User selected
			echo "Normal Mode Selected";

			eval "initdb --username=postgres $POSTGRES_INITDB_ARGS"
		fi

		# Removed here
		# eval "initdb --username=postgres $POSTGRES_INITDB_ARGS"


		# check password first so we can output the warning before postgres
		# messes it up
		file_env 'POSTGRES_PASSWORD'
		if [ "$POSTGRES_PASSWORD" ]; then
			pass="PASSWORD '$POSTGRES_PASSWORD'"
			authMethod=md5
		else
			# The - option suppresses leading tabs but *not* spaces. :)
			cat >&2 <<-'EOWARN'
				****************************************************
				WARNING: No password has been set for the database.
				         This will allow anyone with access to the
				         Postgres port to access your database. In
				         Docker's default configuration, this is
				         effectively any other container on the same
				         system.

				         Use "-e POSTGRES_PASSWORD=password" to set
				         it in "docker run".
				****************************************************
			EOWARN

			pass=
			authMethod=trust
		fi

		if [ "$POSTGRES_REPLICATION_MODE" = 'slave' ] || [ "$POSTGRES_REPLICATION_MODE" = 'master' ]; then
			# check password first so we can output the warning before postgres
			# messes it up
			file_env 'POSTGRES_REPLICATION_PASSWORD'
			if [ "$POSTGRES_REPLICATION_PASSWORD" ]; then
				replPass="PASSWORD '$POSTGRES_REPLICATION_PASSWORD'"
				replAuthMethod=md5
			else
				# The - option suppresses leading tabs but *not* spaces. :)
				cat >&2 <<-'EOWARN'
					****************************************************
					WARNING: No password has been set for the database.
					         This will allow anyone with access to the
					         Postgres port to access your database. In
					         Docker's default configuration, this is
					         effectively any other container on the same
					         system.

					         Use "-e POSTGRES_REPLICATION_PASSWORD=password" to set
					         it in "docker run".
					****************************************************
				EOWARN

				replPass=
				replAuthMethod=trust
			fi
		fi

		{
			echo
			echo "host all all all $authMethod"
		} >> "$PGDATA/pg_hba.conf"

		if [ "$POSTGRES_REPLICATION_MODE" = 'slave' ] || [ "$POSTGRES_REPLICATION_MODE" = 'master' ]; then
			{
				echo
				echo "host replication all all $replAuthMethod"
			} >> "$PGDATA/pg_hba.conf"
		fi

		# internal start of server in order to allow set-up using psql-client
		# does not listen on external TCP/IP and waits until start finishes
		PGUSER="${PGUSER:-postgres}" \
		pg_ctl -D "$PGDATA" \
			-o "-c listen_addresses='localhost'" \
			-w start

		file_env 'POSTGRES_USER' 'postgres'
		file_env 'POSTGRES_DB' "$POSTGRES_USER"

		psql=( psql -v ON_ERROR_STOP=1 )

		if [ "$POSTGRES_REPLICATION_MODE" != 'slave' ]; then
			if [ "$POSTGRES_DB" != 'postgres' ]; then
				"${psql[@]}" --username postgres <<-EOSQL
					CREATE DATABASE "$POSTGRES_DB" ;
				EOSQL
				echo
			fi

			if [ "$POSTGRES_USER" = 'postgres' ]; then
				op='ALTER'
			else
				op='CREATE'
			fi

			"${psql[@]}" --username postgres <<-EOSQL
				$op USER "$POSTGRES_USER" WITH SUPERUSER $pass ;
			EOSQL
			echo
		fi

			# CUSTOM START
		if [ "$POSTGRES_REPLICATION_MODE" = 'master' ]; then
			"${psql[@]}" --username postgres <<-EOSQL
				CREATE USER "$POSTGRES_REPLICATION_USER" REPLICATION LOGIN CONNECTION LIMIT 5 $replPass;
			EOSQL
			echo
			# CUSTOM END
		fi

		psql+=( --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" )

		echo
		for f in /docker-entrypoint-initdb.d/*; do
			case "$f" in
				*.sh)     echo "$0: running $f"; . "$f" ;;
				*.sql)    echo "$0: running $f"; "${psql[@]}" -f "$f"; echo ;;
				*.sql.gz) echo "$0: running $f"; gunzip -c "$f" | "${psql[@]}"; echo ;;
				*)        echo "$0: ignoring $f" ;;
			esac
			echo
		done

		PGUSER="${PGUSER:-postgres}" \
		pg_ctl -D "$PGDATA" -m fast -w stop

		echo
		echo 'PostgreSQL init process complete; ready for start up.'
		echo
	fi
fi

exec "$@"