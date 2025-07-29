# Copyright (c) 2025 FastWeb and/or its affiliates. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Field domain service impl"""

from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.mapper.codegen.field_mapper import FieldMapper
from src.main.app.model.codegen.field_model import FieldModel
from src.main.app.service.codegen.field_service import FieldService


class FieldServiceImpl(
    BaseServiceImpl[FieldMapper, FieldModel], FieldService
):
    def __init__(self, mapper: FieldMapper):
        super().__init__(mapper=mapper)
        self.mapper = mapper
