import os
import h5py
import tempfile
import pandas as pd
from typing import Dict
from pathlib import Path
from smb.SMBConnection import SMBConnection

class TPNFileServer:
    def __init__(self,
        username: str,
        password: str,
        server_ip: str,
        domain_name: str,
        shared_folder: str,
        base_path: str,
        ) -> None:
        self.username = username
        self.password = password
        self.server_ip = server_ip
        self.domain_name = domain_name
        self.shared_folder = shared_folder
        self.server_name = '//{}/'.format(self.server_ip)
        self.base_path = base_path
        self.connection = None

    def getConnection(self):
        connection = SMBConnection(
                        self.username,
                        self.password,
                        self.username,
                        self.server_name,
                        domain = self.domain_name,
                        use_ntlm_v2 = True,
                        is_direct_tcp = True
                    )

        connection.connect(self.server_ip, 445)

        return connection

    def downloadFile(self, input_filepath: str, output_filepath: str, ) -> str:

        with self.getConnection() as connection:
            with open(output_filepath, 'wb') as out_file:
                connection.retrieveFile(
                    self.shared_folder,
                    input_filepath,
                    out_file
                )

        return output_filepath


    def downloadSGSData(self,
                        session_id: int,
                        env_cond_id: int,
                        output_dir: str,
                        filetype: str = 'pos',
                        file_only: bool = True,
                       ) -> str:

        self.session_id = session_id
        self.env_cond_id = env_cond_id

        input_filepath = self.base_path + '/{}/{}/{}.h5'.format(
            session_id,
            str(env_condition_id).zfill(4),
            filetype
        )

        Path(output_dir).mkdir(parents=True, exist_ok=True)
        if file_only:
            filename = '{}_{}_{}.h5'.format(
                session_id,
                str(env_cond_id).zfill(4),
                filetype,
            )
        else:
            filename = os.path.basename(input_filepath)
        output_filepath = os.path.join(output_dir, filename)

        return self.downloadFile(input_filepath, output_filepath)


    def downloadSGSDataAsDataFrame(self,
                        session_id: int,
                        env_cond_id: int,
                        output_dir: str,
                        filetype: str = 'pos',
                        file_only: bool = True,
                       ) -> str:

        self.session_id = session_id
        self.env_cond_id = env_cond_id

        input_filepath = self.base_path + '/{}/{}/{}.h5'.format(
            session_id,
            str(env_cond_id).zfill(4),
            filetype
        )

        Path(output_dir).mkdir(parents=True, exist_ok=True)
        if file_only:
            filename = '{}_{}_{}.csv'.format(
                session_id,
                str(env_cond_id).zfill(4),
                filetype,
            )
        else:
            filename = os.path.basename(input_filepath)
        output_filepath = os.path.join(output_dir, filename)

        df = self.retrieveSGSData(session_id, env_cond_id)
        # df.to_csv(output_filepath)

        return df, filename


    def retrieveSGSData(self,
                        session_id: int,
                        env_cond_id: int,
                        filetype: str = 'pos'
                       ) -> str:

        input_filepath = self.base_path + '/{}/{}/{}.h5'.format(
            session_id,
            str(env_cond_id).zfill(4),
            filetype
        )

        return self.retrieveDataFrameFromH5(input_filepath)


    def retrieveDataFrameFromH5(self, input_filepath: str) -> pd.DataFrame:

        with tempfile.NamedTemporaryFile() as out_file:
            with self.getConnection() as connection:
                connection.retrieveFile(
                    self.shared_folder,
                    input_filepath,
                    out_file
                )
                out_file.seek(0)

                data = self.h5ToDataFrame(
                    os.path.join(tempfile.gettempdir(),out_file.name)
                )

        return data


    def h5ToDataFrame(self,filepath: str) -> Dict:
        data = {}
        with h5py.File(filepath, 'r') as h5:
            datasets = list(h5.keys())
            for dataset in datasets:
                data[dataset] = h5[dataset][()]

        column_names = [
            'x', 'y', 'z', 'xx', 'yy', 'zz',
            'speed_x', 'speed_y', 'speed_z', 'speed_xx', 'speed_yy', 'speed_zz',
            'accel_x', 'accel_y', 'accel_z', 'accel_xx', 'accel_yy', 'accel_zz',
        ]

        df = pd.DataFrame.from_dict(
            dict(zip(column_names, data['time_series_data']))
        )
        df['current_dir'] = data['current_dir']
        df['current_speed'] = data['current_speed']
        df['lines'] = data['lines']
        df['rupture_time'] = data['rupture_time']
        df['session_id'] = data['session_id']
        df['swell_dir'] = data['swell_dir']
        df['swell_hs'] = data['swell_hs']
        df['swell_tp'] = data['swell_tp']
        df['wave_dir'] = data['wave_dir']
        df['wave_hs'] = data['wave_hs']
        df['wave_tp'] = data['wave_tp']
        df['win_dir'] = data['win_dir']
        df['wind_speed'] = data['wind_speed']

        return df
