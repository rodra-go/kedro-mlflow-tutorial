import os
from typing import Dict, List, Iterable
from kedro.config import ConfigLoader
from kedro_mlflow_tutorial.utils.tpn import TPNFileServer
from kedro.config import ConfigLoader


def get_credentials(project_path: str) -> Dict:
    conf_paths = [
        os.path.join(project_path,"conf/base"),
        os.path.join(project_path, "conf/local")
    ]
    conf_loader = ConfigLoader(conf_paths)
    credentials = conf_loader.get("credentials*",
                                  "credentials*/**")

    return credentials


def download_sgs_data(credentials: Dict,
                     sgs_params: Dict,
                     tpn_params: Dict,
                     project_path: str,
                ) -> Dict:

    sgs_base_path = sgs_params['base_path']
    session_ids = sgs_params['download']['session_ids']
    env_condition_ids = sgs_params['download']['env_cond']['ids']
    mode = sgs_params['download']['mode']
    download_dir = sgs_params['download']['dir']
    file_only = sgs_params['download']['file_only']
    start_env_id = sgs_params['download']['env_cond']['start_id']
    end_env_id = sgs_params['download']['env_cond']['end_id']
    env_step = sgs_params['download']['env_cond']['step']

    server_ip = tpn_params['server_ip']
    domain_name = tpn_params['domain_name']
    shared_folder = tpn_params['shared_folder']


    iterable = define_download_data(
        session_ids = session_ids,
        env_ids = env_condition_ids,
        mode = mode,
        start_env_id = start_env_id,
        end_env_id = end_env_id,
        env_step = env_step,
    )

    data = {}
    for session_id, env_id in iterable:
        df, filename = download_sgs_file(
            session_id = session_id,
            env_condition_id = env_id,
            username = credentials['tpn']['username'],
            password = credentials['tpn']['password'],
            server_ip = server_ip,
            domain_name = domain_name,
            shared_folder = shared_folder,
            sgs_base_path = sgs_base_path,
            project_path = project_path,
            download_dir = download_dir
        )
        data[filename] = df

    return data


def define_download_data(
        session_ids: List[int],
        env_ids: List[int] = None,
        mode: str = 'std',
        start_env_id: int = None,
        end_env_id: int = None,
        env_step: int = None,
    ) -> Iterable:
    '''
    Returns an list of tuples (i,j) with i corresponding to the SGS session ID
    and j to the environment condition ID

    Parameters:

    Returns:

    '''

    iterable = []
    if mode == 'std' and env_ids:
        iterable = [(i,j) for i in session_ids
                            for j in env_id]

    elif (mode == 'sparse'
          and start_env_id is not None
          and end_env_id is not None
          and env_step is not None):
        iterable = [(i,j) for i in session_ids
                            for j in range(start_env_id,end_env_id,env_step)]

    return iterable


def download_sgs_file(session_id: int,
                    env_condition_id: int,
                    username: str,
                    password: str,
                    server_ip: str,
                    domain_name: str,
                    shared_folder: str,
                    sgs_base_path: str,
                    project_path: str,
                    download_dir: str = 'data/01_raw/sgs',
                    file_only: bool = True) -> str:

    tpn_client = TPNFileServer(
        username,
        password,
        server_ip,
        domain_name,
        shared_folder,
        sgs_base_path
    )

    if file_only:
        data_dir = download_dir
    else:
        data_dir = os.path.join(download_dir,'/{}/{}'.format(
                        session_id,
                        str(env_condition_id).zfill(4)
                    ))

    output_dir = os.path.join(
        project_path,
        data_dir
    )

    return tpn_client.downloadSGSDataAsDataFrame(
        session_id = session_id,
        env_cond_id = env_condition_id,
        output_dir = output_dir,
        file_only = file_only,
    )
